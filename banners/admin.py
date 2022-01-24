from django.contrib import admin
from .models import Wallpaper, FirstLayerImage, DownlayerImage, AboutUs

@admin.register(Wallpaper)
class WallpaperAdmin(admin.ModelAdmin):
    list_display = ('content', 'redirect_url', 'status', )
    list_display_link = ('content', 'redirect_url', 'status', )



@admin.register(FirstLayerImage)
class FirstLayerImageAdmin(admin.ModelAdmin):
    list_display = ('redirect_url', 'status', )
    list_display_link = ('redirect_url', 'status', )


@admin.register(DownlayerImage)
class DownlayerImageAdmin(admin.ModelAdmin):
    list_display = ('redirect_url', 'status', )
    list_display_link = ('redirect_url', 'status', )



@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    pass