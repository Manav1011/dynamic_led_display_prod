from django.contrib import admin
from datetime import datetime
from .models import SerialCommunication,States,StatesWeekly,Averages
from django.http import HttpResponse
import csv
import xlsxwriter
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)
# Register your models here.

class Actions:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        units = {"WSPD":"Kmph","WDIR":"deg","ATMP":"degC","HUMD":"Per","RAIN":"mm","SRAD":"pm²","BPRS":"mBa","WDCH":"degC","DWPT":"degC"}
        columns = field_names.copy()
        for i,j in enumerate(columns):
            if j in units:
                columns[i] = f"{j} ({units[j]})"
        print(field_names,columns)
        writer.writerow(columns)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected (CSV)"
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(meta)
        
        # Create an XLSX workbook and add a worksheet
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        units = {"WSPD":"Kmph","WDIR":"deg","ATMP":"degC","HUMD":"Per","RAIN":"mm","SRAD":"pm²","BPRS":"mBa","WDCH":"degC","DWPT":"degC"}
        # Write the column headers
        for col_num, field_name in enumerate(field_names):
            if field_name in units:
                field_name = f"{field_name} ({units[field_name]})"
            worksheet.write(0, col_num, field_name)

        # Write the data rows
        for row_num, obj in enumerate(queryset, start=1):
            for col_num, field_name in enumerate(field_names):
                worksheet.write(row_num, col_num, str(getattr(obj, field_name)))

        # Close the XLSX workbook
        workbook.close()

        return response

    export_as_excel.short_description = "Export Selected (Excel)"    


@admin.register(SerialCommunication)
class SerialCommunicationAdmin(admin.ModelAdmin,Actions):
    list_filter = (
        ("RTC", DateRangeQuickSelectListFilterBuilder()),
    )

    actions = ["export_as_csv","export_as_excel","sort_ascending","sort_descending"]
    

class DateAdminDaily(admin.ModelAdmin,Actions):
    date_hierarchy = 'date'  # Specify the DateField you want to filter by date
    actions = ["export_as_csv","export_as_excel","sort_ascending","sort_descending"]

class DateAdminWeekly(admin.ModelAdmin,Actions):
    date_hierarchy = 'date'  # Specify the DateField you want to filter by date
    actions = ["export_as_csv","export_as_excel","sort_ascending","sort_descending"]

admin.site.register(States, DateAdminDaily)
admin.site.register(StatesWeekly, DateAdminWeekly)
admin.site.register(Averages)

