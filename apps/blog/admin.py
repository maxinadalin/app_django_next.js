from django.contrib import admin
from .models import Category,Post, Heading,PostAnalitic



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ("name","title","parent","slug")
    search_fields = ("name","title","parent","slug")
    list_filter = ("parent",)
    ordering = ("name",)
    readonly_fields = ("id",)
    
    
class HeadingInline(admin.TabularInline):
    model = Heading
    extra = 1
    fields = ('title','level','order','slug')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
     list_display = ("status","title","category","slug")
     search_fields = ("status","title","category","slug")
     ordering = ('-created_at',)
     readonly_fields = ("id",'update_at')
     
     fieldsets = (
         ('General information', {
             "fields": (
                 'id',
                 'title',
                 'description',
                 'content',
                 'thumbnail',
                 'keywords',
                 'slug',
                 'category',
             ),
         }),
         (
               'fields & Dates',{
                   'fields': (
                       'created_at',
                       'update_at',
                       'status',
                   )
               },
         )
     )
     inlines = [HeadingInline]
     
     
     
@admin.register(PostAnalitic)
class PostAnaliticAdmin(admin.ModelAdmin):
    list_display = ('post_title','views','impressions','clicks','click_through_rate','avg_time_on_page')
    readonly_fields = ('post_title','views','impressions','clicks','click_through_rate','avg_time_on_page')
    
    def post_title(self,obj):
        return obj.post.title
    
    post_title.short_desciption = 'post_title'