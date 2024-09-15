from django.contrib import admin

from src.django_project.video_app.models import (
    AudioVideoMediaModel,
    ImageMediaModel,
    VideoModel,
)


# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    pass


class AudioVideoMediaAdmin(admin.ModelAdmin):
    pass


class ImageMediaAdmin(admin.ModelAdmin):
    pass


admin.site.register(VideoModel, VideoAdmin)
admin.site.register(AudioVideoMediaModel, AudioVideoMediaAdmin)
admin.site.register(ImageMediaModel, ImageMediaAdmin)
