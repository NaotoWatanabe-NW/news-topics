# Djangoでのアプリケーション作成

アプリケーションの簡易的な作成手順
1. プロジェクト作成
2. 設定ファイル編集
3. モデル作成
4. データベース作成
5. 管理サイト作成
6. フォーム作成
7. フィルタ作成
8. ビュー作成
9. テンプレート作成

## 1. プロジェクト作成
Djangoは最初にコマンドラインを使ってプロジェクトを作成する．
```commandline
mkdir [project]
cd [project]
python -m venv env
env\Scripts\activate
pip install django django-crispy-forms django-filter
django-admin startproject [project] .
python manage.py startapp [app]
```
勝手にフォルダとファイルが作成されるが, サイトのhtmlやcss,フィルタなどのファイルを付け足す必要がある．
```
project
│  manage.py
│  
├─app
│  │  admin.py
│  │  apps.py 
│  │  ★filters.py 
│  │  ★forms.py 
│  │  models.py
│  │  tests.py
│  │  ★urls.py 
│  │  views.py
│  │  __init__.py
│  ├─★static 
│  │  └─★app
│  │      ├─★css 
│  │      │      ★app.css 
│  │      └─★js 
│  │          │  ★app.js 
│  │          └─ ★plugins 
│  │              └─ ★responsive-paginate.js
│  │             
│  ├─migrations
│  │      __init__.py
│  ├─★templates  
│  │  └─★app  
│  │          ★item_card.html 
│  │          ★item_confirm_delete.html 
│  │          ★item_detail.html 
│  │          ★item_filter.html 
│  │          ★item_form.html 
│  │          ★_base.html 
│  │          ★_pagination.html 
│  └─★templatetags 
│          ★item_extras.py 
└─project
        settings.py
        urls.py
        wsgi.py
        __init__.py
```
★マークは自分で作成するファイル
## 2. 設定ファイル編集
[project]フォルダにあるsetting.pyファイルに動作するアプリケーションを追加する．  
ウェブアプリケーションのパッケージをインストールする. 
LOGINの操作を追加する．
```python
# [project]/setting.py
INSTALLED_APPS = [
    'django.contrib.admin',  # 管理者ページ
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',  # 追加
    '[app]',  # 追加
]  # djangoの動かすアプリ

LANGUAGE_CODE = 'ja-JP'  # 日本語
TIME_ZONE = 'Asia/Tokyo'  # タイムゾーン

LOGIN_URL='admin:login'  # LOGINページのURL
LOGOUT_REDIRECT_URL='/'  # LOGOUT後にリダイレクトするURL

# django-crispy-forms 設定
CRISPY_TEMPLATE_PACK = 'bootstrap4'  # BOOTSTRAP4 webアプリケーションフレームワーク
```

## 3. モデル作成
model.pyを編集してモデルを定義する．モデルにはウェブで使うオブジェクトの属性値を定義する．
属性の種類に応じてフィールドを選択する．  
django.db.models: 通常のデータベース sqlite, postgresql, mysqlに対応する  
djongo.models: MongoDBに対応する

```python
# [app]/model.py

from django.db import models
from django.core import validators


class Item(models.Model):

    SEX_CHOICES = (
        (1, '男性'),
        (2, '女性'),
    )

    name = models.CharField(
        verbose_name='名前',
        max_length=200,
    )
    age = models.IntegerField(
        verbose_name='年齢',
        validators=[validators.MinValueValidator(1)],
        blank=True,
        null=True,
    )
    sex = models.IntegerField(
        verbose_name='性別',
        choices=SEX_CHOICES,
        default=1
    )
    memo = models.TextField(
        verbose_name='備考',
        max_length=300,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name='登録日',
        auto_now_add=True
    )

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'アイテム'
        verbose_name_plural = 'アイテム'
```
### フィールドに使えるオプション  
auto_now_add: 追加時に現在時間を設定  
blank: 空白を許すか  
choices: 選択肢を決める  
default: デフォルト値  
max_length: 文字列長  
validators: バリデーションの追加  
verbose_name: 見出し  

## 4. データベース作成
Djangoモデルの定義後にデータベース用のテーブルを作るコマンドを実行する
```commandline
python manage.py makemigrations
python manage.py migrate
```
データベースサーバーを使うときはsetting.pyを変更する  
Djongoを使うときはこんな感じ
```python
# [project]/setting.py
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': '[your-db-name]',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': '[host-name] or [ip address]',
            'port': [port_number],
            'username': '[db-username]',
            'password': '[password]',
            'authSource': '[db-name]',
            'authMechanism': 'SCRAM-SHA-1'
        },
        'LOGGING': {
            'version': 1,
            'loggers': {
                'djongo': {
                    'level': 'DEBUG',
                    'propagate': False,                        
                }
            },
         },
    }
}
```
## 5. 管理サイト作成
Djangoの管理サイトの設定を行う．管理モデルの登録[app]/admin.pyとアプリケーション名の表示[app]/apps.pyを編集する.
```python
# [app]/admin.py

from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass
```
```python
# [app]/apps.py
from django.apps import AppConfig

class SampleAppConfig(AppConfig):
    name = 'app'
    verbose_name = 'アプリ'
```
データベースに管理者ユーザーを作成して, サーバーを起動する  
[http://localhost:8000/admin/] からログインできる
```commandline
python manage.py createsuperuser
python manage.py runserver
```

## 6. フォーム作成
入力フォームを作成する設定クラスを定義する. モデルのもともとの設定に加えられる  
HTMLタグに属性の追加  
```python
# app/forms.py

from django import forms
from .models import Item


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('name','age','sex','memo')
        widgets = {
                    'name': forms.TextInput(attrs={'placeholder':'記入例：山田　太郎'}),
                    'age': forms.NumberInput(attrs={'min':1}),
                    'sex': forms.RadioSelect(),
                    'memo': forms.Textarea(attrs={'rows':4}),
                  }
```

## 7. フィルタ作成
検索フォームを生成する設定クラスを定義する, django-filterを使う  
詳細はdjango-filterを参照
```python
from django_filters import filters
from django_filters import FilterSet
from .models import Item


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = '%s （降順）'


class ItemFilter(FilterSet):

    name = filters.CharFilter(label='氏名', lookup_expr='contains')
    memo = filters.CharFilter(label='備考', lookup_expr='contains')

    order_by = MyOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('name', 'name'),
            ('age', 'age'),
        ),
        field_labels={
            'name': '氏名',
            'age': '年齢',
        },
        label='並び順'
    )

    class Meta:

        model = Item
        fields = ('name', 'sex', 'memo',)
```

## 8. ビュー作成  
クラスベース汎用ビューは組み込みのものでかなり数がある．
- Detail View　データを描画する
- FormView　フォームを描画する
- CreateView　オブジェクトの作成するフォーム
- UpdateView　オブジェクトの保存
- DeleteView　オブジェクトの削除
- ArchiveIndexView　最新のオブジェクトを日付で表示する

[app]/views.pyにビューを定義する. LoginRequiredMixinはログインしていないユーザーをログイン画面に遷移させる設定
```python
# [app]/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .models import Item
from .filters import ItemFilter
from .forms import ItemForm


# Create your views here.
# 検索一覧画面
class ItemFilterView(LoginRequiredMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    # デフォルトの並び順を新しい順とする
    queryset = Item.objects.all().order_by('-created_at')

    # クエリ未指定の時に全件検索を行うために以下のオプションを指定（django-filter2.0以降）
    strict = False

    # 1ページあたりの表示件数
    paginate_by = 10

    # 検索条件をセッションに保存する or 呼び出す
    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)


# 詳細画面
class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item


# 登録画面
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


# 更新画面
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


# 削除画面
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('index')
```

[app]/urls.pyにルーティングを設定する
```python
# [app]/urls.py
from django.urls import path
from .views import ItemFilterView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView


urlpatterns = [
    # 一覧画面
    path('',  ItemFilterView.as_view(), name='index'),
    # 詳細画面
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    # 登録画面
    path('create/', ItemCreateView.as_view(), name='create'),
    # 更新画面
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    # 削除画面
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
]
```
[project]/urls.pyにアプリケーションへのアクセスを可能にする
```python
# [project]/urls.py

from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
```

## 9. テンプレート作成
### 基本方針
Djangoの標準テンプレートは拡張子.htmlのファイルの中に{{}}もしくは%%を使って処理を埋め込む.
テンプレートを部品化して複数のテンプレートを呼び出せる.  
htmlファイルの内容をbodyタグの内部と外部に分けてjavascripライブラリを_base.htmlの共通テンプレートとして内部を作っていく  

### テンプレートタグ
テンプレートでモデル値を使う際にログインユーザーの名前を表示したりするのがテンプレートタグ. 組み込みタグのたくさんある  
- date 日付
- linebreaksbr 改行を<br>に変更
- get_FOO_display choicesの値を使う
- cycle 順に1つずつ値を出力する
- extends 親テンプレートの拡張

クラスベース汎用ビューでtemplateを定義しない場合，モデル名に基づいたテンプレートが呼び出される.
FilterView: item_filter.html
DetailView: item_detail.html
CreateView: item_form.html
UpdateView: item_form.html
DeleteView: item_confirm_delete.html

### ページング機能
ページング機能
```python
# [app]/templatetags/item_extras.py  
from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
```
共通テンプレート
htmlの書き方はいまいちわからない
classタグ: 機能を表す
href: リンク先
meta: 属性
```html
<!-- [app]/templates/app/_base.html -->
{% load static %}
<!DOCTYPE html>
<html lang="ja">

<head>
    <!-- Required meta tags always come first -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>アプリケーション名</title>
    <!-- Bootstrap CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
        crossorigin="anonymous">
    <link href="{% static "[app]/css/app.css" %}" rel="stylesheet">
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">アプリケーション名</a>
        <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#Navber" aria-controls="Navber" aria-expanded="false"
            aria-label="ナビゲーションの切替">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="Navber">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'admin:index'%}">管理サイト</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'admin:logout'%}">ログアウト</a>
                </li>
            </ul>
        </div>
        <!-- /.navbar-collapse -->
    </nav>
    {% block content %} 
    {% endblock %}

    <!-- jQuery first, then Tether, then Bootstrap JS. -->
    <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
        crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <script src="{% static "app/js/plugins/responsive-paginate.js" %}"></script>
    <script src="{% static "app/js/app.js" %}"></script>
</body>

</html>
```
ページング機能
```html
<!-- app/templates.app/_pagination.html -->
{% load item_extras %}
<ul class="pagination">
    {% if page_obj.has_previous %}
        <li class="page-item pagination-prev">
            <a class="page-link" href="?{% url_replace request 'page' page_obj.previous_page_number %}">&laquo;</a>
        </li>
    {% else %}
        <li class="disabled page-item pagination-next">
            <span class="page-link">&laquo;</span>
        </li>
    {% endif %}
    {% for page in page_obj.paginator.page_range %}
        {% if page %}
            {% ifequal page page_obj.number %}
                <li class="active page-item">
                    <span class="page-link">{{ page }}
                        <span class="page-link sr-only">(current)</span>
                    </span>
                </li>
            {% else %}
                <li class="page-item">
                    <a class="page-link" href="?{% url_replace request 'page' page %}">{{ page }}</a>
                </li>
            {% endifequal %}
        {% endif %}
    {% endfor %}
    {% if page_obj.has_next %}
        <li class="page-item pagination-next">
            <a class="page-link" href="?{% url_replace request 'page' page_obj.next_page_number %}">&raquo;</a>
        </li>
    {% else %}
        <li class="disabled page-item pagination-next">
            <span class="page-link ">&raquo;</span>
        </li>
    {% endif %}
</ul>
```

データの詳細を表示
```html
<!-- app/templates/app/item_card.html -->
<div class="row">
    <div class="col-3">
        <p>名前</p>
    </div>
    <div class="col-9">
        <p>{{ item.name }}</p>
    </div>
</div>
<div class="row">
    <div class="col-3">
        <p>年齢</p>
    </div>
    <div class="col-9">
        <p>{{ item.age }}</p>
    </div>
</div>
<div class="row">
    <div class="col-3">
        <p>性別</p>
    </div>
    <div class="col-9">
        <p>{{ item.get_sex_display }}</p>
    </div>
</div>
<div class="row">
    <div class="col-3">
        <p>備考</p>
    </div>
    <div class="col-9">
        <p>{{ item.memo|linebreaksbr }}</p>
    </div>
</div>
<div class="row">
    <div class="col-3">
        <p>登録日</p>
    </div>
    <div class="col-9">
        <p>{{ item.created_at|date:"Y/m/d G:i:s" }}</p>
    </div>
</div>
```
削除画面
```html
<!-- app/templates/app/item_confirm_delete.html -->
{% extends "./_base.html" %}
<!--  -->
{% block content %}
<div class="container">
    <h2 class="text-center">データ削除</h2>
    <p>このデータを削除します。よろしいですか？</p>

    <form action="" method="post">
        {% csrf_token %}
        <div class="row">
            <div class="col-12">
                <div class="float-right">
                    <a class="btn btn-outline-secondary" href="{% url 'index' %}">戻る</a>
                    <input type="submit" class="btn btn-outline-secondary" value="削除" />
                </div>
            </div>
        </div>
        {% include "./item_card.html" %}
        <div class="row">
            <div class="col-12">
                <div class="float-right">
                    <a class="btn btn-outline-secondary" href="{% url 'index' %}">戻る</a>
                    <input type="submit" class="btn btn-outline-secondary" value="削除" />
                </div>
            </div>
        </div>
    </form>
</div>
{% endblock %}
```
詳細画面
```html
<-- [app]/templates/app/item_detail.html -->
{% extends "./_base.html" %}
{% block content %}
<div class="container">
    <h2 class="text-center">詳細表示</h2>
    <div class="row">
        <div class="col-12">
            <a class="btn btn-outline-secondary float-right" href="{% url 'index' %}">戻る</a>
        </div>
    </div>
    <!--  -->
    {% include "./item_card.html" %}
    <div class="row">
        <div class="col-12">
            <a class="btn btn-outline-secondary float-right" href="{% url 'index' %}">戻る</a>
        </div>
    </div>
</div>
{% endblock %}
```

検索一覧画面
```html
<!-- [app]/templates/app/item_filter.html -->
{% extends "./_base.html" %}
{% block content %} 
{% load crispy_forms_tags %}
<div class="container">
    <div id="myModal" class="modal fade" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">検索条件</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="閉じる">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <form id="filter" method="get">
                    <div class="modal-body">
                        {{filter.form|crispy}}
                    </div>
                </form>
                <div class="modal-footer">
                    <a class="btn btn-outline-secondary" data-dismiss="modal">戻る</a>
                    <button type="submit" class="btn btn-outline-secondary" form="filter">検索</button>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-12">
            <a class="btn btn-secondary filtered" style="visibility:hidden" href="/?page=1">検索を解除</a>
            <div class="float-right">
                <a class="btn btn-outline-secondary" href="{% url 'create' %}">新規</a>
                <a class="btn btn-outline-secondary" data-toggle="modal" data-target="#myModal" href="#">検索</a>
            </div>
        </div>
    </div>

    <div class="row" >
        <div class="col-12">
            {% include "./_pagination.html" %}
        </div>
    </div>

    <div class="row">
        <div class="col-12">
            <ul class="list-group">
                {% for item in item_list %}
                <li class="list-group-item">
                    <div class="row">
                        <div class="col-3">
                            <p>名前</p>
                        </div>
                        <div class="col-9">
                            <p>{{ item.name }}</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-3">
                            <p>登録日</p>
                        </div>
                        <div class="col-9">
                            <p>{{item.created_at|date:"Y/m/d G:i:s"}}</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12">
                            <div class="float-right">
                                <a class="btn btn-outline-secondary " href="{% url 'detail' item.pk %}">詳細</a>
                                <a class="btn btn-outline-secondary " href="{% url 'update' item.pk %}">編集</a>
                                <a class="btn btn-outline-secondary " href="{% url 'delete' item.pk %}">削除</a>
                            </div>
                        </div>
                    </div>
                </li>
                {% empty %}
                <li class="list-group-item">
                    対象のデータがありません
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
    <div class="row" >
        <div class="col-12">
            <div class="float-right">
                <a class="btn btn-outline-secondary" href="{% url 'create' %}">新規</a>
                <a class="btn btn-outline-secondary" data-toggle="modal" data-target="#myModal" href="#">検索</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
登録画面・更新画面(共通)
```html
<!-- [app]/templates/app/item_form.html --> 
{% extends "./_base.html" %}
{% load crispy_forms_tags %}
{% block content %}
{{ form.certifications.errors }}
<div class="container">
    <div class="row">
        <div class="col-12">
            <h2 class="text-center">データ入力</h2>
        </div>
    </div>
    <div class="row">
        <div class="col-12">
            <div class="float-right">
                <a class="btn btn-outline-secondary" href="{% url 'index' %}">戻る</a>
                <a class="btn btn-outline-secondary save" href="#">保存</a>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-12">
            <form method="post" id="myform">
                {%crispy form%}
            </form>
        </div>
    </div>
    <div class="row">
        <div class="col-12">
            <div class="float-right">
                <a class="btn btn-outline-secondary" href="{% url 'index' %}">戻る</a>
                <a class="btn btn-outline-secondary save" href="#">保存</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

共通css/js  
[app]/static/app/app.css
```css
.row{
    margin-top:3px;
    margin-bottom:3px;
}
```
### rPage
ページネーションが多いときに画面幅からあふれる分を自動的に省略するプラグイン

```javascript
// 入力フォームでリターンキー押下時に送信させない
$('#myform').on('sumbit', function (e) {
    e.preventDefault();
})

// 連続送信防止
$('.save').on('click', function (e) {
    $('.save').addClass('disabled');
    $('#myform').submit();
})

// [検索を解除] の表示制御
conditions = $('#filter').serializeArray();
$.each(conditions, function(){
    if(this.value){
        $('.filtered').css('visibility','visible')
    }
})

// ページネーションのレスポンシブ対応
// https://auxiliary.github.io/rpage/
$(".pagination").rPage();
```
