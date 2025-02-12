from django.db import models
from django.contrib.auth.models import User

#イベント投稿機能
class Post(models.Model):
    event_name = models.CharField(verbose_name='イベント名', max_length=255)
    live_name = models.CharField(verbose_name='ライブ名', max_length=255) #使われてない？
    live_time = models.DateTimeField(verbose_name='日付', blank=True, null=True)
    open_time = models.DateTimeField(verbose_name='開場時間')
    event_time = models.DateTimeField(verbose_name='イベント時間')
    # place = models.CharField(verbose_name='公演場所', max_length=500)
    place = models.ForeignKey('Venue', verbose_name='会場', on_delete=models.CASCADE, null=True, blank=True)# 会場選択
    price = models.IntegerField(verbose_name='料金')
    number = models.PositiveIntegerField(verbose_name='チケット枚数', default=0)  # デフォルト値を設定
    remaining_tickets = models.PositiveIntegerField(verbose_name='残りチケット枚数', default=0)
    resale_tickets = models.PositiveIntegerField(verbose_name='再販チケット枚数', default=0)
    total_sold_tickets = models.IntegerField(verbose_name='購入済みのチケット枚数',default=0) 
    limit = models.TextField(verbose_name='申し込み制限', blank=True, null=True)
    payment = models.TextField(
        verbose_name='支払い方法',
        choices=[
            ('cash', 'コンビニ支払い'),
            ('credit_card', 'クレジットカード'),
            ('QR payment', 'QR決済'),
        ],
    )
    period = models.DateTimeField(verbose_name='販売終了日')
    winning = models.DateTimeField(verbose_name='当落発表日')
    payment_fin = models.DateTimeField(verbose_name='お支払い期限')
    attention = models.TextField(verbose_name='注意事項', blank=True, null=True)
    category = models.CharField(
        verbose_name='カテゴリ',
        max_length=50,
        choices=[
            ('detail', '会場見え方'),
            ('ticket', '飲食'),
            ('stage', '交通情報'),
        ],
        default='detail'  # デフォルト値を設定
    )
    comment = models.TextField(verbose_name='イベント詳細情報', blank=True)
    image = models.ImageField(verbose_name='画像', upload_to='uploads/posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
   #venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')

    def save(self, *args, **kwargs):
         # `remaining_tickets` を `number` の値で初期化
        if self.remaining_tickets == 0:  # デフォルト値が0のときのみ更新
            self.remaining_tickets = self.number
    # チケットの枚数を更新する際に残り枚数と再販枚数を管理
        if self.remaining_tickets < 0:
            self.remaining_tickets = 0
        if self.resale_tickets < 0:
            self.resale_tickets = 0
    #残り枚数を計算する
        if self.total_sold_tickets > 0:
            self.remaining_tickets = self.number - self.resale_tickets - self.total_sold_tickets
            
        # self.total_sold_tickets = self.number - self.remaining_tickets  # total_sold_ticketsの更新
        super().save(*args, **kwargs)
            
    def __str__(self):
        return f"{self.event_name} - {self.place} on {self.event_time.strftime('%Y-%m-%d')}"
    
#お問い合わせ
class Connect(models.Model):
    
    # username = models.CharField(verbose_name='ユーザー名')
    # useremail =models.CharField(verbose_name='メールアドレス')
    sendtime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(verbose_name='主な内容',max_length=50)
    contents = models.TextField(verbose_name='内容')
    image =models.ImageField(verbose_name='画像',upload_to='connectimage',blank=True,null=True)

#ブックマーク機能    
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Post', on_delete=models.CASCADE)  # イベント(Postモデル)と関連付け
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # 同じユーザーが同じイベントを複数ブックマークできない

# チケット申し込み履歴
class TicketHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 申し込みをしたユーザー
    event = models.ForeignKey('Post', on_delete=models.CASCADE)  # 関連イベント
    status = models.CharField(
        verbose_name='申し込みステータス',
        max_length=50,
        choices=[
            ('pending', '結果待ち'),
            ('won', '当選'),
            ('lost', '落選'),
            ('canceled', 'キャンセル')  # キャンセルステータスを追加
        ],
        default='pending'
    )
    is_resale = models.BooleanField(default=False)  # 再販申し込みかどうかのフラグ
    application_date = models.DateTimeField(verbose_name='申し込み日時', auto_now_add=True)  # 申し込み日時
    result_date = models.DateTimeField(verbose_name='当選発表日')  # 当選発表日

    def __str__(self):
        return f"{self.event.event_name} - {self.status} ({self.user.username})"

            
#会場情報の入力
class Venue(models.Model):
    name = models.CharField(verbose_name='会場名', max_length=255)
    address = models.TextField(verbose_name='住所')
    phone_number = models.CharField(verbose_name='電話番号', max_length=50, blank=True, null=True)
    #google_map_url = models.URLField(verbose_name='GoogleマップURL', blank=True, null=True) #max_length=1000,
    floor_map = models.ImageField(verbose_name='フロアマップ', upload_to='uploads/venues/', blank=True, null=True)
    capacity = models.PositiveIntegerField(verbose_name='収容人数', blank=True, null=True)
    additional_info = models.TextField(verbose_name='追加情報', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    generate_iframe = models.TextField(max_length=1024, null=True,blank=True)  # Googleマップの埋め込みURLを格納

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # GoogleマップURLの自動設定（例: generate_iframeにGoogleマップの埋め込みURLを設定）
        if not self.generate_iframe and self.address:
            # ここでGoogleマップのURLを設定するロジックを追加
            self.generate_iframe = f"https://www.google.com/maps/embed/v1/place?q={self.address}&key=YOUR_GOOGLE_MAPS_API_KEY"
        super().save(*args, **kwargs)
    
    """# iframeタグの生成
    def generate_iframe(self):
        if self.google_map_url and "embed" in self.google_map_url:
            return f'<iframe src="{self.google_map_url}" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
        return None"""
#座席からの見え方の画像
class VenueImage(models.Model):
    venue = models.ForeignKey(Venue, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='venue_images/')
    name = models.CharField(max_length=255, blank=True, null=True)  # 画像名フィールドを追加

    def __str__(self):
        return self.name if self.name else "画像"


#お問い合わせ返信
class Connectreply(models.Model):
    
    connect = models.ForeignKey(Connect, related_name='replies', on_delete=models.CASCADE)
    sendtime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(verbose_name='主な内容',max_length=50,blank=False,default='')
    contents = models.TextField(verbose_name='内容',blank=False,default='')
    image =models.ImageField(verbose_name='画像',upload_to='connectimage',blank=True,default='')

#決済からマイページ
class Ticket(models.Model):
    user = models.ForeignKey(User,verbose_name='購入者', on_delete=models.CASCADE) # チケット所有者のユーザー情報
    #（ユーザーが削除されるとチケットも削除される）
    post = models.ForeignKey(Post, verbose_name='関連イベント', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0,verbose_name='購入枚数')# デフォルト値を整数に変更
    is_canceled = models.BooleanField(verbose_name='キャンセル済み', default=False)
    purchase_date = models.DateTimeField(verbose_name='購入日', auto_now_add=True)
    event_date = models.DateField()  # イベントの日付
    venue = models.CharField(max_length=255)  # 会場の名前
    seat_row = models.CharField(max_length=10)  # 座席の列
    seat_number = models.CharField(max_length=10)  # 座席番号
    seat_type = models.CharField(max_length=10)  # 座席の種類（例：VIP、一般）
    price = models.DecimalField(max_digits=10, decimal_places=2)  # チケットの価格
    #qr_code = models.ImageField(upload_to='qr_codes/') # QRコードの画像ファイル
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('pending', '保留'), ('paid', '支払い済み')], default='pending')

    def cancel_ticket(self):
        """チケットキャンセル処理"""
        if not self.is_canceled:
            self.is_canceled = True
            self.save()
            # 再販用チケット枚数に追加
            self.post.resale_tickets += self.quantity
            self.post.save()
    
    def __str__(self):
        return f"{self.user.username} - {self.event_date} - {self.venue}"
     # ユーザー名、イベント日付、会場名を表示
     
class Comment(models.Model):
    CATEGORY_CHOICES = [
        ('seat_view', '座席からの見え方'),
        ('event', 'イベント'),
        ('transport', '交通情報'),
    ]
    
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)  # 画像のアップロード

    def __str__(self):
        return f"Comment by {self.user.username} on {self.event.event_name}"
    
    #def __str__(self):
        #return f"{self.user.username} - {self.category}"


class ReTicket(models.Model):
    re_title = models.CharField(verbose_name='イベント名', max_length=255)
    re_price = models.IntegerField(verbose_name='料金')
    re_image = models.ImageField(verbose_name='画像', upload_to='uploads/posts/', blank=True, null=True)
    re_remaining_tickets = models.PositiveIntegerField(verbose_name='残りチケット枚数', default=0)
    re_resale_tickets = models.PositiveIntegerField(verbose_name='再販チケット枚数', default=0)

    
# キャンセルチケット
class TicketCancellation(models.Model):
    post = models.ForeignKey(Post, related_name="cancellations", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)  # 管理者の承認が必要

    def approve(self):
        # 承認処理: 承認されると再販チケットに反映
        if self.is_approved:
            post = self.post
            post.resale_tickets += self.quantity
            post.save()
