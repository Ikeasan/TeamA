import os
from pathlib import Path

# プロジェクトディレクトリのパス
BASE_DIR = Path(__file__).resolve().parent.parent

# セキュリティキー
SECRET_KEY = 'django-insecure-t60%j@bge4k5k+ys207@8+b#^2x&r=!=wc48tovhye&&$__p$8'

# デバッグモード
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'False'

# 許可されるホスト
ALLOWED_HOSTS = ['Ikesan.pythonanywhere.com']

# アプリケーション
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'ticket_app',  # カスタムアプリケーション
    'qr_code',#QRコード
    # 'ticket_app.apps.TicketAppConfig',
]

# ミドルウェア
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',     # 追加
]

# URL設定
ROOT_URLCONF = 'ticket_line.urls'

# テンプレート設定
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # カスタムテンプレート
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # allauth 必須
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGIアプリケーション（エラーが出るためいったん消してる）
WSGI_APPLICATION = 'ticket_line.wsgi.application'

# データベース設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# パスワードバリデーター
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ロケール設定
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# プロジェクトの静的ファイルのURL
STATIC_URL = '/static/'

STATIC_ROOT ='/static'

# 開発環境で静的ファイルを探すディレクトリ
STATICFILES_DIRS = [
    BASE_DIR / "static",  # プロジェクト直下のstaticディレクトリ
]

# デフォルトのプライマリキー設定
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 認証バックエンド
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# メッセージフレームワーク（Bootstrap対応）
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# リダイレクト設定
LOGIN_REDIRECT_URL = '/'  # ログイン後のリダイレクト先
LOGOUT_REDIRECT_URL = '/accounts/login/'  # ログアウト後のリダイレクト先
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'  # ログアウト後のリダイレクト先（allauth用）

# メール認証関連
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # メール認証を必須
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # ユーザー名またはメールアドレスでログイン可能
ACCOUNT_SIGNUP_FIELDS = ['username', 'email', 'password1', 'password2']

# メール認証完了後のリダイレクト先
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/accounts/login/'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/accounts/login/'

# メールリンククリック時に認証を完了
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# メールバックエンド
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 開発環境用
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 本番環境用
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@example.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_ROOT = BASE_DIR / 'media'
# MEDIA_ROOT = BASE_DIR.joinpath('media')
CSRF_COOKIE_NAME = "csrftoken"