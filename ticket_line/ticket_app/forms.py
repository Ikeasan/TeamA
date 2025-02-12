from allauth.account.forms import SignupForm   # なんか警告出てるけど今のところ問題ないので無視
from django import forms
from django.forms import modelformset_factory
from .models import Post
from django.shortcuts import render
from .models import Connect
from .models import Venue,VenueImage
from .models import Connectreply
from .models import Ticket
from .models import Comment

class CustomSignupForm(SignupForm):
    username = forms.CharField(
        max_length=30,
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )

    def save(self, request):
        user = super().save(request)
        # ここで追加の処理が可能 (例: プロフィール作成)
        return user
    
    def OPE_post(request):
        return render(request, 'OPE_post')  # OPE_post.htmlテンプレートを表示
     
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'image', 'event_name', 'open_time', 'event_time', 'place', 
            'price', 'number', 'limit', 'payment', 'period','winning','payment_fin','comment'
        ]
        widgets = {
            'live_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'open_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'event_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'period': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'winning': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'payment_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'attention': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # 注意事項を複数行に
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 60, 'placeholder': 'イベントの詳細を入力してください'}),  # 説明を複数行に
        }
        venue = forms.ModelChoiceField(
            queryset=Venue.objects.all(),
            label='会場',
            widget=forms.Select,
        )
    
#イベント検索
class EventSearchForm(forms.Form):
    query = forms.CharField(
        label="イベントを検索",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'キーワードを入力'})
    )
    
#問い合わせ        
class ConnectForm(forms.ModelForm):
    class Meta:
        model = Connect
        fields = [
            'title','contents','image' 
        ]

# 問い合わせ返信        
class ConnectreplyForm(forms.ModelForm):
    class Meta:
        model = Connectreply
        fields = [
            'title','contents','image' 
        ]

#会場  
class VenueForm(forms.ModelForm):
     class Meta:
        model = Venue
        fields = ['name', 'address', 'phone_number', 'floor_map', 'capacity', 'additional_info']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            #'google_map_url': forms.URLInput(attrs={'class': 'form-control'}),
            'floor_map': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
        def clean_google_map_url(self):
            url = self.cleaned_data.get('google_map_url')
            if url and not (url.startswith('http://') or url.startswith('https://')):
                url = 'http://' + url  # 自動的に「http://」を補完
            return url

#会場の座席画像
class VenueImageForm(forms.ModelForm):
    class Meta:
        model = VenueImage
        fields = ['image','name']  # name フィールドを追加/ 画像と名前
        
    image = forms.ImageField(required=False)  # ← ここを追加
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': '画像名を入力'}))
# フォームセット（座席画像フォーム）を作成（最大15個の画像）
VenueImageFormSet = modelformset_factory(VenueImage, form=VenueImageForm, extra=15, can_delete=True) # 削除機能を有効化 #ここの数字で投稿数管理
"""class Meta:
        model = Venue
        fields = ['name', 'address','phone_number','google_map_url','floor_map','capacity','additional_info']
        widgets = {
            # 'details': forms.Textarea(attrs={'rows': 4}),
            'floor_map': forms.ClearableFileInput(attrs={'required': False}),  # ファイル選択を任意に
            #'address': forms.Textarea(attrs={'rows': 3}),
        }"""
        
        
# マイページのチケット表示
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event_date', 'venue', 'seat_row', 'seat_number', 'seat_type', 'price', 'qr_code']
       
        
#コメント機能
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['image','content', 'category']
        widgets = {
            'category': forms.Select(choices=Comment.CATEGORY_CHOICES),
        }