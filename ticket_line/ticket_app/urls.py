from django.urls import path
from . import views


### 画像認識用インポート ###
from django.conf import settings
from django.conf.urls.static import static
##########################

from django.views.generic import TemplateView
from .views import event_list
from .views import venue_create_view


from .views import check_event_results

urlpatterns = [
    # ホームページ
    path('', views.home_view, name='home'),
    
    #Googleマップ2/6
    path("venue/create/", venue_create_view, name="venue_create"),  # URLが正しいか確認

    
    # 利用規約?お試し
    path('Terms', views.Terms_view, name='Terms_of_User'),
    
    #イベント検索　(利用者)
    path('events/', event_list, name='event_search_results'),
    
    # イベント検索（運営者）
    path('ope_search/', views.ope_search_results, name='ope_search_results'),
    
    #マイページのパスワード変更
    #path('password-reset-done2/', TemplateView.as_view(template_name='password_reset_done2.html'), name='password_reset_done2'),

    # メール確認リンクの処理
    path('accounts/confirm-email/<str:key>/', views.confirm_email_and_redirect, name='account_confirm_email'),
    
    # マイページ
    path('mypage/', views.mypage_view, name='mypage'),

    # プライバシーポリシー
    path('policy/', views.policy_view, name='policy'),

    # 投稿一覧（PostListViewを関数型ビューに置き換えた場合）
    # path('posts/', views.post_list_view, name='post_list'),

    #運営者
    
    path('ope_del/', views.ope_del_view, name='ope_del'),

    path('ope_eve/', views.ope_eve_view, name='ope_eve'),
    
    path('ope_top/', views.ope_top_view, name='ope_top'),
    
    path('ope_post/', views.ope_post_view, name='ope_post'),
    
    # path('ope_post_submit/', views.ope_post_submit, name='ope_post_submit'),
    
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),  # 編集用URL
    
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'), #削除
    

    # 以下管理者
    
    #会場
    path('venue/create/', views.venue_create_view, name='venue_create'),
    path('venue/list/', views.venue_list_view, name='venue_list'),
    path('edit_venue/<int:venue_id>/', views.edit_venue, name='edit_venue'),
    path('delete_venue/<int:venue_id>/', views.delete_venue, name='delete_venue'),
    path('venue/create/done/', views.venue_create_done_view, name='venue_create_done'),


    
    #管理者TOP画面<管理者>
    path('ad_ticket', views.Ad_Ticket, name='AD_TOP'),

    #キャンセルチケット受け取り<管理者>
    path('ad_ticket/ad_tic', views.AD_Ticketcancell, name='AD_Ticketcancell'),
    
    #キャンセル枚数管理<管理者>
    path('ad_ticket/ad_Winnigs', views.AD_Winnings, name='AD_Random'),

    #問い合わせフォーム<管理者>
    path('ad_connect/', views.ad_connect_view, name='ad_connect'),
    
    #問い合わせフォーム削除<管理者>
    path('ad_connect_del/<int:pk>/', views.ad_connect_delete, name='ad_connect_del'),
    
    #問い合わせフォーム返信<管理者>
    path('ad_connect_reply/<int:pk>/', views.ad_connect_reply_view, name='ad_connect_reply'),

    path('ad_reply/<int:pk>', views.ad_connect_reply_view, name='ad_reply'),

    #再度投稿<管理者>
    path('ad_repost/', views.ad_repost_view, name='ad_repost'),

    #キャンセル枚数管理 抽選<管理者>
    path('ad_uid/', views.ad_uid_view, name='ad_uid'),

    #以上管理者
    
    #ブックマーク機能
    path('bookmark/', views.bookmark_view, name='bookmark'),
    path('bookmark_toggle/<int:post_id>/', views.bookmark_toggle, name='bookmark_toggle'),
    path('bookmark/list/', views.bookmark_list, name='bookmark_list'),

    #コメント機能
    path('comment/', views.comment_view, name='comment'),
    path('comments/', views.comment_list, name='comment_list'),


    #イベント
    path('event/<int:event_id>/', views.event_view, name='event_detail'),
    
    # #再販申し込み
    # path('re_ticket/<int:event_id>/', views.re_ticket_view, name='re_ticket'),

    #再販チケット申し込み
    path('event/<int:event_id>/get_re_ticket/', views.get_re_ticket_view, name='get_re_ticket'),

    
    #チケット申し込み
    path('event/<int:event_id>/get_ticket/', views.get_Ticket2_view, name='getTicket2'),
    
    path('event/<int:event_id>/', views.event_view, name='event_detail'),
    #チケット申し込み完了
    path('getTicketdone/<int:event_id>/', views.get_Ticketdone_view, name='getTicketdone'),

    #以下運営者

    #削除<運営者>
    path('ope_del/', views.ope_del_view, name='ope_del'),

    #イベント管理<運営者>
    path('ope_eve/', views.ope_eve_view, name='ope_eve'),

    #投稿<管理者>
    path('ope_post/', views.ope_post_view, name='ope_post'),

    #運営者TOP<運営者>
    path('ope_top/', views.ope_top_view, name='ope_top'),

    #以上運営者

    #利用規約
    path('policy/', views.policy_view, name='policy'),

    #QRコード
    path('qr/<int:ticket_id>', views.qr_view, name='qr'),
    
    

    #会場
    path('stage/', views.stage_view, name='stage'),

    #チケット申し込み履歴
    path('ticket-history/', views.ticket_history_view, name='ticket_history_url'),
    path('submit_ticket/', views.submit_ticket, name='submit_ticket'),
    #申込情報を保存
    path('apply/<int:event_id>/', views.apply_ticket_view, name='apply_ticket'),
    path('re_apply/<int:event_id>/', views.apply_re_ticket_view, name='apply_re_ticket'),
    
    # 再販チケット専用
    path('re_ticket_wg/<int:event_id>/', views.re_ticket_wg_view, name='re_ticket_wg'),
    path('re_payment/<int:event_id>/<int:ticket_id>/', views.re_payment_view, name='re_payment_view'),
    path('re_pay_done/<int:ticket_id>/', views.re_pay_done, name='re_pay_done'),
    path('re_pay_done_success/<int:ticket_id>/', views.re_pay_done_success, name='re_pay_done_success'),
    
    #当落を出す
    path('check_event_results/<int:event_id>/', check_event_results, name='check_event_results'),
    #当選内容表示
    path('events/<int:event_id>/check_results/', views.check_ticket_result_view, name='check_ticket_result_view'),
    
#お試し
    # 当落確認ページへのランダム遷移（成功）
    path('check_ticket_result/', views.check_ticket_result_view, name='check_ticket_result'),
    
    #当落確認-1
    path('ticket/<int:event_id>/wg/', views.ticket_wg_view, name='ticket_wg'),
    
    # 支払い手続きページ
    path('ticket/<int:event_id>/payment/<int:ticket_id>/', views.payment_view, name='payment_view'),
    
    #支払処理
    path('pay_done/<int:ticket_id>/', views.pay_done, name='pay_done'),
    
    # 成功画面
    path('payment/success/<int:ticket_id>/', views.pay_done_success, name='pay_done_success'),
    
    #チケット表示
    path('ticket_adv/', views.ticket_adv, name='ticket_adv'),
    
    #各チケット表示
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    
    #チケットキャンセル
    path('cancel_ticket/<int:ticket_id>/', views.cancel_ticket, name='cancel_ticket'),
    
    #キャンセル完了
    path('cancel_done/<int:ticket_id>/', views.cancel_done_view, name='cancel_done'),
    
    path('submit_resale_ticket/', views.submit_resale_ticket, name='submit_resale_ticket'),

    #ユーザー投稿
    path('userpost/', views.user_post_view, name='userpost'),
    #利用者用お問い合わせ
    path('connect/', views.connect_view, name='connect'),
    
    path('connect_view/', views.connect_view, name='connect_view'),
    #コピーの呼び出し
    path('ticket_copy/<int:post_id>/',views.reticketcopy, name='ticket_copy'),
    
    #デバック
    path('debug/',views.debug_view, name='debug'),
        
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 画像認識コード


# MEDIA_URL を開発環境で提供する設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
