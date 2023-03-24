from django.contrib import admin

# Register your models here.
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

from reservation.models import *


class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'show_capacity', 'is_reserved', 'show_categories')
    list_display_links = ('id',)
    list_editable = ('is_reserved',)
    list_filter = ('category', 'capacity', 'is_reserved')
    search_fields = ('description', 'category')
    filter_horizontal = ('category',)

    def show_capacity(self, obj):
        url = reverse('admin:reservation_table_change', args=(obj.id,))
        return mark_safe(f'<a href="{url}">{obj.capacity} человек(а)</a>')

    show_capacity.short_description = 'Вместимость'

    def show_categories(self, obj):
        categories = ', '.join(map(lambda e: e.name, obj.category.all()))
        return categories

    show_categories.short_description = 'Категории'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'show_tables')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')

    def show_tables(self, obj):
        tables = Table.objects.filter(category__in=[obj])

        url = (
                reverse("admin:reservation_table_changelist")
                + "?"
                + urlencode({"category__id__exact": f"{obj.id}"})
        )
        return mark_safe(f'{tables.count()} <a href="{url}" target="_blank">(просмотреть)</a>')

    show_tables.short_description = 'Столики с данной категорией'


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'visit_date', 'visit_time', 'table', 'phone', 'client', 'is_finishing')
    list_display_links = ('id', 'visit_date', 'visit_time')
    list_editable = ('is_finishing',)
    list_filter = ('created_at', 'visit_date', 'visit_time', 'count', 'is_finishing')
    search_fields = ('phone',)


class ReservationHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'visited_at', 'reservation', 'served', 'total', 'show_client')
    list_display_links = ('id', 'visited_at', 'reservation', 'served', 'total')
    list_filter = ('total', 'served', 'visited_at')
    search_fields = ('id', 'reservation__phone')
    autocomplete_fields = ('served', 'reservation')

    def show_client(self, obj):
        return obj.reservation.client

    show_client.short_description = 'Гость'


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'show_preview')
    list_display_links = ('id', 'description')
    search_fields = ('description',)

    def show_preview(self, obj):
        url = reverse('admin:reservation_photo_change', args=(obj.id,))

        if obj.image:
            return mark_safe(f'<a href="{url}"><img height="150px" src="/media/{obj.image}" /></a>')
        return 'Изображение отсутствует'

    show_preview.short_description = 'Превью'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'show_reservation_history', 'show_served', 'show_reservation_date')
    list_display_links = ('id', 'author')
    search_fields = ('author', 'description', 'reservation_history')
    autocomplete_fields = ('reservation_history',)
    
    def show_reservation_history(self, obj):
        url = reverse('admin:reservation_reservationhistory_change', args=(obj.reservation_history.pk, ))
        return mark_safe(f'{obj.reservation_history} <a href="{url}" target="_blank">(просмотреть)</a>')
    
    show_reservation_history.short_description = 'История бронирования'

    def show_reservation_date(self, obj):
        return obj.reservation_history.reservation.visit_date
    
    show_reservation_date.short_description = 'Дата посещения'

    def show_served(self, obj):
        return obj.reservation_history.served
    show_served.short_description = 'Обслуживал(а)'


class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'visit_date', 'visit_time', 'count', 'phone')
    list_display_links = ('id', 'name')
    list_filter = ('visit_date', 'visit_time', 'count')
    search_fields = ('phone', 'name')


admin.site.register(Table, TableAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservationHistory, ReservationHistoryAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Request, RequestAdmin)
