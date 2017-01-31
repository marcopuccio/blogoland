# Blogoland
Just another Django Blog app.

<br>
## Requirements

Blogoland is developed and require Django>=1.9, pillow, Python > 2.7 and django-summernote.

<br>
## How to install it

It can be installed via pip running the next command.
```
pip install git+http://github.com/marcopuccio/blogoland.git
```

After installation, you must include it in your ```settings.py```. You can add it via the app config file, or the appname. In adition, you must include the WYSIWYG editor [Django Summernote](https://github.com/summernote/django-summernote) dependency.

```
INSTALLED_APPS = [
    # WYSIWYG editor dependency
    'django_summernote',

    ...
    # Blogoland App Config
    'blogoland.apps.BlogolandConfig',
    ...
    # Blogoland appname
    'blogoland',
]
```
Then add it in ```urls.py```:
```
urlpatterns = [
    ...
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'', include('blogoland.urls')),
    ]
```
Finally, run the migration executing ```python manage.py migrate```

**Congrats, it's ready!***

<br>
## Settings

You can set some variables in your Django *settings* file to modify custom behavior of this package.

```BLOGOLAND_PAGINATION```: Alter pagination(default=15)

```BLOGOLAND_DATE_FORMAT```: Alter the date representation(default=```'%d-%m-%Y'```). Used to nice render the date in templates. 
 
<br>
## Default URLs and Views

|      View name      |URL                           | Args   |
|---------------------|------------------------------|--------|
|`post_list`          |`/`                           |None    |
|`post_detail`        |`/<post_slug>/`               |String  |
|`category_post_list` |`/category/<category_slug>/`  |String  |

<br>
***POST_LIST***

Returns the list of public posts. This QuerySet is paginated(Default=15 post).

Template name:
```
"blogoland/post_list.html"
```
<br>
***POST_DETAIL***

Returns the Detail of the Post.

Templates Hierarchy:
```
"blogoland/post_<post_slug>.html"
"blogoland/post_detail.html"
```
<br>
***CATEGORY_POST_LIST***

Returns the detail of the category and a list of Posts related to a it.The post QuerySet is paginated(Default=15 post). 

Templates Hierarchy:
```
"blogoland/category_<category_slug>_list.html"
"blogoland/category_post_list.html"
```

<br>
## Template tags

*comming soon...*
