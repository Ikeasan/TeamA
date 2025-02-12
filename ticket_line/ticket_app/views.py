from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from allauth.account.models import EmailConfirmation
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from ticket_app.models import Post, TicketHistory
from .models import Connect
from .forms import ConnectForm
from ticket_app.models import Connect
from django.utils.timezone import now
from .models import Bookmark, Post
from .models import Post, TicketHistory, Ticket
from django.utils import timezone
from .forms import VenueForm,VenueImageForm,VenueImageFormSet
from .models import Venue,VenueImage
from .models import Connectreply
from .forms import ConnectreplyForm
from ticket_app.models import Connectreply
from .models import Ticket # マイページのチケット表示
from .forms import TicketForm # これも
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
import random
from .models import Comment
from .forms import CommentForm
from django.utils.timezone import now
from .models import ReTicket
from .models import ReTicket
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging
from .forms import EventSearchForm
from django.urls import reverse
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings


# 利用規約？お試し
@login_required
def Terms_view(request):
    return render(request, 'Terms_of_User.html')
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404

#お試し　イベント検索　成功(利用者)
@login_required
def event_list(request):
    #form = EventSearchForm(request.GET or None)  # フォームのインスタンス
    query = request.GET.get('query', '')  # クエリ文字列を取得
    events = Post.objects.all()  # 全てのイベントを取得

    #if form.is_valid():  # フォームが有効な場合
    if query:  # 検索キーワードが入力された場合
        events = events.filter(event_name__icontains=query)  # 部分一致でフィルタリング


    return render(request, 'event_search_results.html', {'events': events})

@login_required
def home_view(request):
    query = request.GET.get('query', '')  # 検索キーワードを取得
    events = Post.objects.filter(name__icontains=query) if query else None  # 部分一致で検索
    posts = Post.objects.all()  # すべてのイベントを取得
    return render(request, 'home.html', {'posts': posts,'events': events, 'query': query})

# 運営者（イベント検索）仮
@login_required
def ope_search_results(request):
    query = request.GET.get('query', '')  # 検索ワードを取得
    events = Post.objects.all()  # 初期状態で全イベントを取得
    
    if query:
        # 部分一致検索
        events = events.filter(event_name__icontains=query)
    
    return render(request, 'ope_search_results.html', {'events': events, 'query': query})


"""
#運営者（イベント検索）　仮
@login_required
def ope_search_results(request):
    query = request.GET.get('query', '')
    events = Post.objects.all()  # 全てのイベントを取得
    #events = Post.objects.filter(event_name__icontains=query) if query else []
    
    if query: # 検索キーワードが入力された場合
        events = Post.objects.filter(event_name__icontains=query) # 部分一致でフィルタリング
    else:
        events = Post.objects.all()
    return render(request, 'ope_search_results.html', {'events': events, 'query': query})
    """
@login_required
def confirm_email_and_redirect(request, key):
    """
    メール確認リンクをクリックしただけで認証を完了し、ログインページへリダイレクト
    """
    email_confirmation = get_object_or_404(EmailConfirmation, key=key)
    if not email_confirmation.email_address.verified:
        email_confirmation.confirm(request)
        messages.success(request, "メールアドレスの確認が完了しました！")
    else:
        messages.info(request, "このメールアドレスはすでに認証されています。")
    
    # ログインページにリダイレクト
    return redirect(reverse("account_login"))

@login_required
def mypage_view(request):
    """
    マイページを表示するビュー
    """
    return render(request, 'mypage.html')

@login_required
def policy_view(request):
    """
    プライバシーポリシーを表示するビュー
    """
    return render(request, 'policy.html')

#以下運営者

#削除<運営者>
@login_required
def ope_del_view(request):
    return render(request, 'OPE_del.html')

#イベント画面<運営者>
@login_required
def ope_eve_view(request):
    return render(request, 'OPE_eve.html')

#イベントTOPページビュー (OPE_TOP.html)
@login_required
def ope_top_view(request):
    posts = Post.objects.all()  # イベント情報を全て取得
    return render(request, 'OPE_TOP.html', {'posts': posts})

#イベント投稿
@login_required
def ope_post_view(request):
    # return render(request, 'connect.html')
    posts =Post
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "内容を送信しました。")
            return redirect('ope_top')  # 送信後にリダイレクト
        else:
            messages.error(request, "フォームにエラーがあります。再度入力してください。")
            return render(request, 'OPE_post.html', {'form': form})  # エラー時に再度フォームを表示
    else:
        # CONNECT以外のリクエストは拒否
        form = PostForm()
    return render(request, 'OPE_post.html', {'form': form, 'posts': posts})
    # return redirect('connect')  # フォーム画面にリダイレクト


#イベント編集
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('ope_top')  # 編集後にTOP画面へリダイレクト
    else:
        form = PostForm(instance=post)
    return render(request, 'OPE_eve.html', {'form': form, 'post': post})



#イベント削除
def delete_post(request, post_id):
    if request.method == 'POST':  # POSTリクエストのみ受け付ける
        post = get_object_or_404(Post, id=post_id)
        post.delete()  # 該当のPostを削除
        return redirect('ope_top') 
    
#以上運営者


#以下管理者

#会場登録完了
@login_required
def venue_create_done_view(request):
    return render(request, 'venue_create_done.html')

"""#会場登録(使わないかも）
@login_required
def venue_create_view(request):
    if request.method == 'POST':  # フォーム送信時の処理
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():  # フォームが有効な場合
            form.save()  # データベースに保存
            return redirect('venue_create_done')  # 完了画面へリダイレクト
        else:
            # バリデーションエラーの場合、エラーメッセージを表示
            messages.error(request, "フォームにエラーがあります。再度入力してください。")
    else:  # GETリクエスト時の処理
        form = VenueForm()

    return render(request, 'venue_create.html', {'form': form})"""
    
# maps.json の読み込み関数
def load_map_urls():
    json_path = os.path.join(os.path.dirname(__file__), 'maps.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
   
# 会場のマップURLを定義
MAP_URLS = { 
    "東京ドーム": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6479.673102947879!2d139.75189129999998!3d35.70563959999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60188c4782eed4f3%3A0x5058b288249e640e!2z5p2x5Lqs44OJ44O844Og!5e0!3m2!1sja!2sjp!4v1738801715191!5m2!1sja!2sjp",
    "京セラドーム": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3281.422673100756!2d135.4761427!3d34.669280400000005!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6000e7b24b87684b%3A0x535f75f9161484f1!2z5Lqs44K744Op44OJ44O844Og5aSn6Ziq!5e0!3m2!1sja!2sjp!4v1738801751742!5m2!1sja!2sjp",
    "福岡PayPayドーム": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3323.3819024789454!2d130.36212319999998!3d33.5953942!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3541924d02e6b64b%3A0xb79cd978d2ed54c2!2z44G_44Ga44G7UGF5UGF544OJ44O844Og56aP5bKh!5e0!3m2!1sja!2sjp!4v1738801780319!5m2!1sja!2sjp"
}

# 会場の登録
@login_required
def venue_create_view(request):
    selected_venue = ""  # 初期値
    map_url = ""  # 初期値

    # 会場名と地図URLの対応を定義
    MAP_URLS = {
        "東京ドーム": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6479.673102947879!2d139.75189129999998!3d35.70563959999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60188c4782eed4f3%3A0x5058b288249e640e!2z5p2x5Lqs44OJ44O844Og!5e0!3m2!1sja!2sjp!4v1738801715191!5m2!1sja!2sjp",
        "京セラドーム": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3281.422673100756!2d135.4761427!3d34.669280400000005!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6000e7b24b87684b%3A0x535f75f9161484f1!2z5Lqs44K744Op44OJ44O844Og5aSn6Ziq!5e0!3m2!1sja!2sjp!4v1738801751742!5m2!1sja!2sjp",
        "福岡PayPayドーム": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3323.3819024789454!2d130.36212319999998!3d33.5953942!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3541924d02e6b64b%3A0xb79cd978d2ed54c2!2z44G_44Ga44G7UGF5UGF544OJ44O844Og56aP5bKh!5e0!3m2!1sja!2sjp!4v1738801780319!5m2!1sja!2sjp",
        # 他の会場も追加
    }

    # GETリクエストで会場名を取得
    selected_venue = request.GET.get('venue_name', '')  # クエリパラメータやフォームから取得

    if request.method == 'POST':
        # POSTリクエストで会場名を取得
        selected_venue = request.POST.get("venue_name", "").strip()
        map_url = MAP_URLS.get(selected_venue, "")  # マップURL取得
        """
        #今追加した試し
        if selected_venue:
            # Googleマップの埋め込みURLを直接設定
            map_url = f"https://www.google.com/maps/embed/v1/place?key=YOUR_GOOGLE_MAPS_API_KEY&q={selected_venue}"
            # セッションに保存
            request.session["selected_venue"] = selected_venue
            request.session["map_url"] = map_url
    """

        # デバッグ用ログ
        print(f"選択された会場: {selected_venue}")
        print(f"対応するマップURL: {map_url}")
        
        form = VenueForm(request.POST, request.FILES)
        formset = VenueImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            venue = form.save()  # 会場情報を保存

            # 画像フォームの保存
            for image_form in formset:
                image = image_form.save(commit=False)
                image.venue = venue  # 画像を保存した会場に紐付け
                image.save()

            return redirect('venue_list')  # 会場リストページへリダイレクト

    else:
        form = VenueForm()
        formset = VenueImageFormSet(queryset=VenueImage.objects.none())

    context = {
        'form': form,
        'formset': formset,
        'selected_venue': selected_venue,
        'map_url': map_url,  # JSONから取得した地図URLを渡す
    }

    return render(request, 'venue_create.html', context)
"""{
        'form': form,
        'formset': formset,
        'selected_venue': selected_venue,
        'map_url': map_url   # JSONから取得した地図URLを渡す
    })"""
    
#会場一覧
@login_required
def venue_list_view(request):
    
    # Venue と関連する VenueImage のデータを効率的に取得
    venues = Venue.objects.prefetch_related('images').order_by('-id')
   # # 投稿一覧を降順で取得（例: idの降順で並び替え
  # venues = Venue.objects.all().order_by('-id')  # venues を取得
    for venue in venues:
        print(venue.id)  # venue.id が正しいかを確認する
    return render(request, 'venue_list.html', {'venues': venues})



#会場編集 (文字とフロアマップはできるが、座席の編集不可)
@login_required
def edit_venue(request, venue_id):  
    venue = get_object_or_404(Venue, id=venue_id)  # 会場を取得
    venue_images = VenueImage.objects.filter(venue=venue)  # 既存の座席画像を取得

    # `VenueImageFormSet` を定義（座席画像の編集用）
    VenueImageFormSet = modelformset_factory(VenueImage, form=VenueImageForm, extra=1, can_delete=True)

    if request.method == 'POST':
        print("🛠 [DEBUG] POST request received")  # デバッグ用
        print("🛠 [DEBUG] request.FILES:", request.FILES)  # デバッグ用
        
        form = VenueForm(request.POST, request.FILES, instance=venue)  # 会場情報フォーム
        formset = VenueImageFormSet(request.POST, request.FILES, queryset=venue_images)  # 座席画像フォームセット

        if form.is_valid() and formset.is_valid():
            print("✅ [DEBUG] form and formset are valid")  # デバッグ用
            # 会場情報の更新
            venue = form.save(commit=False)
            instances = formset.save(commit=False)
            
            # フロアマップの更新
            if 'floor_map' in request.FILES:
                venue.floor_map = request.FILES['floor_map']

            venue.save()
            
            print("🛠 [DEBUG] venue saved:", venue)  # デバッグ用

            # 座席画像の追加・編集
            instances = formset.save(commit=False)
            print("🛠 [DEBUG] formset cleaned data:", formset.cleaned_data)  # デバッグ用

            for instance in instances:
                if instance.image:  # 画像がある場合のみ更新
                    instance.venue = venue
                    instance.save()
                print("🛠 [DEBUG] Saving image:", instance.image)  # デバッグ用
                instance.save()

            # 削除処理
            for instance in formset.deleted_objects:
                print("🛠 [DEBUG] Deleting image:", instance)  # デバッグ用
                instance.delete()

            print("✅ [DEBUG] All changes saved successfully")  # デバッグ用

            return redirect(reverse('venue_list'))  # 編集完了後にリスト画面へ
        else:
            print("❌ [DEBUG] Form or formset is invalid")  # デバッグ用
            print("❌ [DEBUG] Form errors:", form.errors)  # デバッグ用
            print("❌ [DEBUG] Formset errors:", formset.errors)  # デバッグ用


    else:
        print("🛠 [DEBUG] GET request received")  # デバッグ用
        form = VenueForm(instance=venue)
        formset = VenueImageFormSet(queryset=venue_images)

    return render(request, 'venue_eve.html', {
        'form': form,
        'venue': venue,
        'formset': formset,
    })
"""def edit_venue(request, venue_id):  # post_id -> venue_idに変更
    venue = get_object_or_404(Venue, id=venue_id)  # Venueを取得する
    venue_images = VenueImage.objects.filter(venue=venue)# 既存の座席画像を取得
    
    if request.method == 'POST':
        # 会場情報のフォームと座席画像のフォームセットを一度に処理
        form = VenueForm(request.POST, request.FILES, instance=venue)  # Venueフォーム（会場情報＋フロアマップ）
        formset = VenueImageFormSet(request.POST, request.FILES, queryset=venue_images) # 座席画像フォームセット

        form_valid = form.is_valid()
        formset_valid = formset.is_valid()

        if form_valid or formset_valid:  # どちらかが有効なら処理を進める
            if form_valid:  # 会場情報（フロアマップ含む）が変更された場合
                venue = form.save(commit=False)

                # 新しいフロアマップがアップロードされた場合
                if 'floor_map' in request.FILES:
                    venue.floor_map = request.FILES['floor_map']

                venue.save()  # フロアマップと会場情報を保存
            
            if formset_valid:  # 座席画像が変更された場合
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.venue = venue  # 会場と紐付ける
                    instance.save()

                # 削除対象の画像を処理
                for instance in formset.deleted_objects:
                    instance.delete()

            return redirect(reverse('venue_list'))  # 編集後に会場リストへリダイレクト
            
    else:
        form = VenueForm(instance=venue)
        formset = VenueImageFormSet(queryset=venue_images)

    return render(request, 'venue_eve.html', {
        'form': form,
        'venue': venue,
        'formset': formset,
    })"""
    
"""
# 会場編集
def edit_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)  # 会場を取得
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)  # フォームをインスタンスとともに使用
        if form.is_valid():
            form.save()  # フォームを保存して更新する
            return redirect(reverse('venue_list'))  # 編集後に会場リストにリダイレクト
    else:
        form = VenueForm(instance=venue)  # GETリクエストの場合は現在の会場情報をフォームに渡す

    return render(request, 'venue_eve.html', {'form': form, 'venue': venue})"""

#会場削除
def delete_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    #venue = Venue.objects.get(id=venue_id)
    if request.method == 'POST':  # POSTリクエストのみ受け付ける
        #venue = get_object_or_404(Venue, id=venue_id)  # Venueモデルでvenue_idを使って取得
        venue.delete()  # 該当のVenueを削除
        return redirect(reverse('venue_list'))  # 会場リストにリダイレクト
    return render(request, 'delete_venue.html', {'venue': venue})

#管理者TOP<管理者>
@login_required
def Ad_Ticket(request):
    return render(request, 'AD/AD_TOP.html')


#当落確認<管理者>
@login_required
def AD_Winnings(request):
    return render(request,'AD/AD_RandomST.html')

#問い合わせ<管理者>
@login_required
def ad_connect_view(request):
    connects = Connect.objects.all()
    return render(request, 'AD/AD_connect.html',{'connects' : connects })

#問い合わせ削除<管理者>
@login_required
def ad_connect_delete(request, pk):
        connect = get_object_or_404(Connect, pk=pk)
        connect.delete()  # 該当のPostを削除
        return redirect('ad_connect') 
    
#問い合わせ返信画面<管理者>
@login_required
def ad_connect_reply(request,pk):
    return render(request, 'AD/AD_connect_reply.html')   

@login_required
def ad_connect_list(request):
    connects = Connect.objects.prefetch_related('replies').all()
    return render(request,'AD/ad_connect.html',{'connects':connects,})

#再投稿<管理者>
@login_required
def ad_repost_view(request):
    return render(request, 'AD/AD_Repost.html')

#チケット購入フォーム
@login_required
def purchase_ticket_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    ticket_numbers = range(1, post.remaining_tickets + 1)  # 残りチケット枚数分の選択肢を作成
    if request.method == 'POST':
        number_of_tickets = int(request.POST.get('number', 0))  # 購入枚数を取得
        if number_of_tickets <= post.remaining_tickets:
            post.remaining_tickets -= number_of_tickets
            post.total_sold_tickets += number_of_tickets
            post.save()
            messages.success(request, f'{number_of_tickets} 枚のチケットを購入しました。')
            return redirect('success_page')  # 購入後のリダイレクト先
        else:
            messages.error(request, '残りのチケット枚数が足りません。')
    
    return render(request, 'payment.html', {
        'post': post,
        'ticket_numbers': ticket_numbers  # テンプレートに渡す
    })


#チケット枚数管理<管理者>　元
@login_required
def ad_uid_view(request):
    return render(request, 'AD/AD_UID.html')


#キャンセルチケット受け取り<管理者> 　元
@login_required
def AD_Ticketcancell(request):
    return render(request, 'AD/AD_CancelPick.html')

# キャンセル時にチケット枚数更新
@login_required
def cancel_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if not ticket.is_canceled:
        ticket.cancel_ticket()
        messages.success(request, f"{ticket.quantity}枚のチケットをキャンセルしました。")
    else:
        messages.error(request, "このチケットは既にキャンセルされています。")
    
    return redirect('ticket_history')

#再販チケット申し込み　元
@login_required
def get_re_ticket_view(request):
    return render(request, 'GetReTicket.html')

"""# 管理者がキャンセルを承認する際に、再販チケットとして反映?
@login_required
def approve_cancellation(request, cancellation_id):
    cancellation = get_object_or_404(TicketCancellation, id=cancellation_id)
    if request.user.is_staff:  # 管理者だけが承認できる
        cancellation.is_approved = True
        cancellation.save()
        cancellation.post.resale_tickets += cancellation.quantity
        cancellation.post.save()
        messages.success(request, "キャンセルが承認され、再販チケットとして反映されました。")
    return redirect('admin_dashboard')"""

# 再販チケット購入でチケット枚数減らすカウント
@login_required
def purchase_resale_ticket(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    quantity = int(request.POST.get('quantity', 1))

    if post.resale_tickets >= quantity:
        post.resale_tickets -= quantity
        post.save()

        Ticket.objects.create(user=request.user, post=post, quantity=quantity)
        messages.success(request, f"再販チケットを{quantity}枚購入しました！")
    else:
        messages.error(request, "再販チケットが不足しています。")
    
    return redirect('ope_post', post_id=post_id)



#以上管理者

#ブックマーク機能
@login_required
def bookmark_view(request):
    # ユーザーのブックマークを取得
    bookmarks = Bookmark.objects.filter(user=request.user)  # ログインしているユーザーのブックマークを取得
    return render(request, 'Bookmark.html', {'bookmarks': bookmarks})

@login_required
def bookmark_toggle(request, post_id):
    event = get_object_or_404(Post, id=post_id)
    # ブックマークがすでに存在しているか確認
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, event=event)
    
    if not created:
        # すでにブックマークされている場合は削除
        bookmark.delete()
    
    # ブックマークされた場合でも削除された場合でも、元のイベントページにリダイレクト
    return redirect('event_detail', event_id=event.id)

@login_required
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('event')
    return render(request, 'bookmark.html', {'bookmarks': bookmarks})

#コメント機能
@login_required
def comment_view(request):
    return render(request, 'comment.html')

#イベント画面
@login_required
def event_view(request, event_id):
    event = get_object_or_404(Post, id=event_id)
    venue = event.place

    # カテゴリー別にコメントを取得
    seat_view_comments = Comment.objects.filter(event=event, category='seat_view')
    event_comments = Comment.objects.filter(event=event, category='event')
    transport_comments = Comment.objects.filter(event=event, category='transport')

    # ユーザーがブックマークしているかどうかの判定
    is_bookmarked = Bookmark.objects.filter(user=request.user, event=event).exists()


    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.event = event
            new_comment.user = request.user
            new_comment.save()

            # コメント投稿後にブックマーク状態を更新
            if not is_bookmarked:
                Bookmark.objects.create(user=request.user, event=event)

            return redirect('event_detail', event_id=event.id)  # ここは 'event_detail' に修正
    else:
        form = CommentForm()

    return render(request, 'Event.html', {
        'event': event,
        'venue': venue,
        'seat_view_comments': seat_view_comments,
        'event_comments': event_comments,
        'transport_comments': transport_comments,
        'form': form,
        'is_bookmarked': is_bookmarked,  # ブックマーク状態をテンプレートに渡す
    })

from django.shortcuts import get_object_or_404

#イベント画面会場画面
@login_required
def event_detail_view(request, event_id):
    # イベント情報を取得
    event = get_object_or_404(Post, id=event_id)

    # 紐付けられた会場情報を取得
    venue = event.venue  # イベントモデルに会場情報が関連付けられている場合

    # テンプレートにデータを渡す
    return render(request, 'event_detail.html', {
        'event': event,
        'venue': venue,
    })

#チケット申し込みボタン押す
@login_required
def get_Ticket2_view(request, event_id):
    event = get_object_or_404(Post, id=event_id)  # イベントを取得
    ticket_numbers = range(1, event.number + 1)  # 選択可能な枚数を定義
   

    return render(request, 'getTicket2.html', {
        'event': event,
        'ticket_numbers': ticket_numbers
    })

#申し込み完了ボタン
@login_required
def apply_ticket_view(request, event_id):
    # イベント情報を取得
    event = get_object_or_404(Post, id=event_id)

    if request.method == "POST":
        # フォームから枚数を取得
        ticket_count = request.POST.get('tickets')

        # チケット枚数の確認
        if not ticket_count or not ticket_count.isdigit() or int(ticket_count) <= 0:
            messages.error(request, "正しい枚数を選択してください。")
            return render(request, 'getTicket2.html', {'event': event, 'ticket_numbers': range(1, 11)})

        # `result_date`の設定: `Post`モデルの`winning`フィールドを使用
        result_date = event.winning if event.winning else now()

        # チケット履歴を作成
        TicketHistory.objects.create(
            user=request.user,
            event=event,
            status="pending",  # デフォルトステータス
            application_date=now(),
            result_date=result_date  # `Post`モデルの`winning`を設定
        )

        # 成功メッセージを表示し、完了画面へリダイレクト
        messages.success(request, "申し込みが完了しました！")
        return redirect('getTicketdone', event_id=event.id)

    # GETリクエスト時
    return render(request, 'getTicket2.html', {'event': event, 'ticket_numbers': range(1, 11)})

#チケット申し込み完了画面
@login_required
def get_Ticketdone_view(request, event_id):
    # 必要に応じてイベントを取得
    event = get_object_or_404(Post, id=event_id) #modelsの所から情報持ってきてる
    #event_id = 1  # 例: イベントIDを取得する処理
    context = {
        'event_id': event_id,
        'event': event,  # テンプレートでイベント情報を表示するため
    }
    return render(request, 'getTicketdone.html', context)

#利用者用 問い合わせ
@login_required
def connect_view(request):
    # return render(request, 'connect.html')
    posts =Connect
    connects = Connect.objects.all()
    reply =Connectreply.objects.all()
    if request.method == 'POST':
        form = ConnectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "内容を送信しました。")
            return redirect('connect')  # 送信後にリダイレクト
        else:
            messages.error(request, "フォームにエラーがあります。再度入力してください。")
            return render(request, 'connect.html', {'form': form})  # エラー時に再度フォームを表示
    else:
        # CONNECT以外のリクエストは拒否
        form = ConnectForm()
    return render(request, 'connect.html', {'form': form, 'posts': posts, 'connects': connects, 'reply': reply })
    # return redirect('connect')  # フォーム画面にリダイレクト
    
#問い合わせ返信処理<管理者>
@login_required
def ad_connect_reply_view(request,pk):
    connect = get_object_or_404(Connect,pk=pk)
    replies = Connectreply.objects.filter(connect=connect)
    # connects = Connectreply.objects.all()
    if request.method == 'POST':
        form = ConnectreplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.connect = connect
            reply.save()
            messages.success(request, "内容を送信しました。")
            return redirect('ad_connect')  # 送信後にリダイレクト
        else:
            messages.error(request, "フォームにエラーがあります。再度入力してください。")
            print(form.errors)
            return render(request, 'AD/ad_connect_reply.html', {'form': form, 'connect': connect, 'replies': replies})  # エラー時に再度フォームを表示
    else:
        # CONNECT以外のリクエストは拒否
        form = ConnectreplyForm()
    
    print(connect.pk)
    
    return render(request, 'AD/ad_connect_reply.html', {'form': form, 'connect' : connect, 'replies': replies})
    # return redirect('connect')  # フォーム画面にリダイレクト    

#利用規約
@login_required
def policy_view(request):
    return render(request, 'policy.html')

#QRコード表示
@login_required
def qr_view(request,ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # event= get_object_or_404(Post, id=event_id) 
    return render(request, 'QR.html', {'ticket': ticket})

#会場
@login_required
def stage_view(request):
    return render(request, 'stage.html')

# チケット申し込み履歴表示
@login_required
def ticket_history_view(request):
    today = timezone.now().date()  # 現在の日付（時刻を含まない）

    upcoming_tickets = TicketHistory.objects.filter(
        user=request.user,
        status__in=['pending', 'won', 'lost', 'canceled'],
        event__event_time__gt=timezone.now()
    )

    past_tickets = TicketHistory.objects.filter(
        user=request.user,
        status__in=['pending', 'won', 'lost', 'canceled'],
        event__event_time__lt=timezone.now()
    )

    return render(request, 'ticket_history.html', {
        'upcoming_tickets': upcoming_tickets,
        'past_tickets': past_tickets,
        'today': today  # 日付のみ渡す
    })
    
#チケットを申し込む
def submit_ticket(request):
    if request.method == 'POST':
        # 必要なデータを取得
        event_id = request.POST.get('event_id')  # フォームからイベントIDを取得
        result_date = request.POST.get('result_date')  # 当選発表日
        is_resale = request.POST.get('is_resale', False)  # 再販フラグ (デフォルトはFalse)

        # イベント情報を取得
        event = Post.objects.get(id=event_id)

        # 再販の場合、イベント名を「再販: イベント名」に加工
        if is_resale:
            event_name = f"再販: {event.event_name}"
        else:
            event_name = event.event_name

        # TicketHistoryを保存
        TicketHistory.objects.create(
            user=request.user,
            event=event,
            result_date=result_date,
            status='pending',  # 初期ステータスは結果待ち
        )

        # チケット履歴ページへリダイレクト
        return redirect('ticket_history')

    # POST以外のリクエストではエラーを返す
    return render(request, 'submit_ticket.html')

# ログの設定
logger = logging.getLogger(__name__)

# イベント当選結果処理(改良)
# @csrf_exempt
def check_event_results(request, event_id):
    try:
        if request.method != "POST":
            return JsonResponse({"success": False, "message": "無効なリクエストです。"})

        # ログ出力
        logger.info(f"Event ID: {event_id} リクエスト受信")

        event = get_object_or_404(Post, id=event_id)
        ticket_histories = TicketHistory.objects.filter(event=event, status="pending")
        logger.info(f"応募者数: {ticket_histories.count()}")

        # 応募者がいない場合の処理
        if ticket_histories.count() == 0:
            return JsonResponse({"success": False, "message": "応募者がいません。"})

        # チケットの総数を取得
        total_tickets = event.number  # イベントのチケット総数（number）
        max_winners = min(ticket_histories.count(), total_tickets)  # 当選者数は応募者数と総チケット数の少ない方に制限

        # ランダムに当選者を選ぶ
        with transaction.atomic():
            try:
                winners = random.sample(list(ticket_histories), max_winners)  # 当選者をランダムに選ぶ
                winners_ids = [winner.id for winner in winners]

                # 当選者のステータスを更新
                for winner in ticket_histories:
                    if winner.id in winners_ids:
                        winner.status = "won"  # 当選に変更
                    else:
                        winner.status = "lost"  # 落選に変更
                    winner.save()

                # 当選者にチケットを発行
                for winner in winners:
                    ticket = Ticket.objects.create(
                        user=winner.user,
                        post=event,  # どのイベントのチケットかを指定
                        quantity=1,  # 当選者が1枚購入（仮定）
                        event_date=event.event_time.date(),  # イベントの日時
                        venue=event.place.name if event.place else "未定",  # 会場名（Noneの場合の処理）
                        seat_row="A",  # 座席行（仮定）
                        seat_number="1",  # 座席番号（仮定）
                        seat_type="VIP",  # 座席タイプ（仮定）
                        price=event.price  # チケット価格（イベント価格を使用）
                    )
                    logger.info(f"当選者 {winner.user.username} にチケットが発行されました。")

                logger.info(f"当選者: {', '.join([winner.user.username for winner in winners])}、落選者数: {len(ticket_histories) - len(winners)}")

            except Exception as e:
                logger.error(f"トランザクション内でエラーが発生しました: {str(e)}")
                return JsonResponse({"success": False, "message": "エラーが発生しました。管理者にお問い合わせください。"})

        return JsonResponse({"success": True, "message": "当選処理が完了しました。"})

    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        return JsonResponse({"success": False, "message": "エラーが発生しました。管理者にお問い合わせください。"})

# チケット結果確認ビュー
@login_required
def check_ticket_result_view(request, event_id):
    if request.method == 'POST':
        try:
            # 該当のチケット履歴を取得
            ticket = get_object_or_404(TicketHistory, event_id=event_id, user=request.user)

            # `status` フィールドの値を確認
            if ticket.status == 'won':
                return JsonResponse({
                    'success': True,
                    'message': 'おめでとうございます！当選しました。',
                    'redirect_url': '/ticket_wg/'  # 当選ページ
                })
            elif ticket.status == 'lost':
                return JsonResponse({
                    'success': False,
                    'message': '残念ながら落選しました。',
                    'redirect_url': '/ticket_wg2/'  # 落選ページ
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'まだ結果が発表されていません。',
                })
        
        except TicketHistory.DoesNotExist:
            logger.error(f"チケット履歴が見つかりませんでした。Event ID: {event_id}, User: {request.user.username}")
            return JsonResponse({'success': False, 'message': '該当のチケット履歴が見つかりません。'}, status=404)
        except Exception as e:
            logger.error(f"エラーが発生しました: {str(e)}")
            return JsonResponse({'success': False, 'message': 'エラーが発生しました。管理者にお問い合わせください。'}, status=500)

    return JsonResponse({'success': False, 'message': '無効なリクエストです。'}, status=400)

#当選ページへ
@login_required
def ticket_wg_view(request, event_id):
    # チケットの確認
    ticket = Ticket.objects.filter(post_id=event_id, user=request.user).order_by('-event_date').first()

    if ticket is None:
        return HttpResponseNotFound("チケットが見つかりません。")

    # 🔍 `TicketHistory` に `status` がある場合、そのデータを取得
    ticket_history = TicketHistory.objects.filter(event=ticket.post, user=request.user).order_by('-result_date').first()

    if ticket_history:
        if ticket_history.status == 'won':
            # 再販チケットか通常チケットかを判定
            if ticket_history.is_resale:
                # 再販チケットの場合の処理
                payment_url = reverse('payment_view_resale', kwargs={'event_id': event_id, 'ticket_id': ticket.id})
                return render(request, 'TicketWG_resale.html', {'ticket': ticket, 'payment_url': payment_url})
            else:
                # 通常チケットの場合の処理
                payment_url = reverse('payment_view', kwargs={'event_id': event_id, 'ticket_id': ticket.id})
                return render(request, 'TicketWG.html', {'ticket': ticket, 'payment_url': payment_url})
        else:
            return redirect('ticket_history_url')
    else:
        return redirect('ticket_history_url')


logger = logging.getLogger(__name__) # ロガーの設定

#お支払い入力画面へ
@login_required
def payment_view(request, event_id, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)  
    return render(request, 'payment.html', {'tickets': [ticket]})

# ロガーの設定
logger = logging.getLogger(__name__)

# 支払い完了ボタン処理
@login_required
def pay_done(request, ticket_id):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=ticket_id)

        # 購入処理後にチケットの状態を更新
        ticket.status = "paid"  # 'paid' のフラグ
        ticket.save()

        # チケットが関連付けられている Post（イベント）を取得
        event = ticket.post

        # Postのtotal_sold_ticketsを1増やす
        event.total_sold_tickets += 1
        event.save()

        # 購入完了ページにリダイレクト
        return redirect('pay_done_success', ticket_id=ticket.id)  # ticket_id を渡す
    return HttpResponseBadRequest("無効なリクエストです。")

# 成功メッセージ画面
@login_required
def pay_done_success(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # 合計金額を計算
    total_price = ticket.quantity * ticket.price

    return render(request, 'payment_success.html', {
        'ticket': ticket,
        'total_price': total_price
    })

#チケット表示
@login_required
def ticket_adv(request):
    tickets = Ticket.objects.filter(user=request.user, status="paid")  # paid のみ取得
    return render(request, 'TicketADV.html', {'tickets': tickets})

#各チケット
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})

# チケットキャンセル処理（ステータスのみ変更）
@login_required
def cancel_ticket(request, ticket_id):
    # チケット情報を取得
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    # POSTリクエストの処理（キャンセル処理）
    if request.method == 'POST':
        # キャンセル理由やその他のフォーム情報を処理
        # cancel_reason = request.POST.get('cancel_reason')
        ticket.is_canceled = True
        # ticket.cancel_reason = cancel_reason  # キャンセル理由を保存（カラムがある場合）
        ticket.save()

        return redirect('cancel_done', ticket_id=ticket.id)  # キャンセル完了画面へリダイレクト

    # GETリクエスト時にはチケット情報をテンプレートに渡す
    return render(request, 'CancelTicket.html', {'ticket': ticket})

    
# キャンセル完了処理
@login_required
def cancel_done_view(request, ticket_id):
    try:
        # キャンセル対象のチケットを取得
        ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
        
        # TicketHistoryのステータスを更新
        ticket_history = get_object_or_404(TicketHistory, event=ticket.post, user=request.user)
        ticket_history.status = 'canceled'
        ticket_history.save()
        
        # チケットが所属するPostを取得
        post = ticket.post

        # Postのチケット数を更新 (再販チケット数を増加し、購入済みチケット数を減少)
        post.resale_tickets += 1
        post.total_sold_tickets -= 1
        post.save()
        
        # チケットを削除
        ticket.delete()

        # キャンセル完了画面を表示
        return render(request, 'CancelDone.html')

    except (Ticket.DoesNotExist, TicketHistory.DoesNotExist):
        return JsonResponse({"success": False, "message": "チケットまたは履歴が見つかりません。"})




# #再販チケット申し込み
# @login_required
# def get_re_ticket_view(request):
#     return render(request, 'GetReTicket.html')

#再販申し込み
@login_required
def get_re_ticket_view(request, event_id):
    event = get_object_or_404(Post, id=event_id)  # イベントを取得
    # 再販チケットがある場合のみ表示
    if event.resale_tickets >= 1:
        ticket_numbers = range(1, event.resale_tickets + 1)  # 再販チケット枚数の範囲
        return render(request, 'GetReTicket.html', {
            'event': event,
            'ticket_numbers': ticket_numbers,
            'is_resale': True  # 再販フラグ
        })
    # 再販チケットがない場合は通常のチケットページに遷移
    return redirect('event_detail', event_id=event.id)

#再販申し込みボタン
@login_required
def apply_re_ticket_view(request, event_id):
    event = get_object_or_404(Post, id=event_id)

    if request.method == "POST":
        ticket_count = request.POST.get('tickets')
        is_resale = request.POST.get('is_resale') == 'true'  # フォームから再販フラグを取得

        # チケット枚数の確認
        if not ticket_count or not ticket_count.isdigit() or int(ticket_count) <= 0:
            messages.error(request, "正しい枚数を選択してください。")
            return render(request, 'GetReTicket.html', {'event': event, 'ticket_numbers': range(1, 11), 'is_resale': True})

        # `result_date`の設定
        result_date = event.winning if event.winning else now()

        # チケット履歴を作成
        TicketHistory.objects.create(
            user=request.user,
            event=event,
            status="pending",  # 初期ステータス
            application_date=now(),
            result_date=result_date,
            is_resale=is_resale  # 再販フラグを保存
        )

        # 成功メッセージを表示
        messages.success(request, "申し込みが完了しました！")
        return redirect('getTicketdone', event_id=event.id)

    # GETリクエスト時
    return render(request, 'GetReTicket.html', {'event': event, 'ticket_numbers': range(1, 11), 'is_resale': True})

#再販完了画面
@login_required
def get_Ticketdone_view(request, event_id):
    event = get_object_or_404(Post, id=event_id)
    # TicketHistory から該当の履歴を取得
    ticket_history = TicketHistory.objects.filter(user=request.user, event=event).order_by('-application_date').first()
    is_resale = ticket_history.is_resale if ticket_history else False  # 再販かどうか

    context = {
        'event_id': event_id,
        'event': event,
        'is_resale': is_resale,  # 再販フラグ
    }
    return render(request, 'getTicketdone.html', context)



# 再販チケット用 当選ページへ
@login_required
def re_ticket_wg_view(request, event_id):
    # チケットの確認
    ticket = Ticket.objects.filter(post_id=event_id, user=request.user).order_by('-event_date').first()

    if ticket is None:
        return HttpResponseNotFound("チケットが見つかりません。")

    # 再販チケットの申し込み履歴を取得
    ticket_history = TicketHistory.objects.filter(event=ticket.post, user=request.user, is_resale=True).order_by('-result_date').first()

    if ticket_history:
        if ticket_history.status == 'won':  # is_resale はすでに True なので不要
            # 再販チケットの当選ページへ
            payment_url = reverse('re_payment_view', kwargs={'event_id': event_id, 'ticket_id': ticket.id})
            return render(request, 'TicketWG_resale.html', {'ticket': ticket, 'payment_url': payment_url})
        else:
            return redirect('ticket_history_url')  # 当選していない場合は履歴へ戻る
    else:
        return HttpResponseNotFound("再販チケットの履歴が見つかりません。")





# 再販チケット用 支払い入力画面
@login_required
def re_payment_view(request, event_id, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'payment_resale.html', {'tickets': [ticket]})


# 再販チケット用 支払い完了処理
@login_required
def re_pay_done(request, ticket_id):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=ticket_id)

        # 購入処理後にチケットの状態を更新
        ticket.status = "paid"  # 'paid' のフラグ
        ticket.save()

        # チケットが関連付けられている Post（イベント）を取得
        event = ticket.post

        # Postのtotal_sold_ticketsを1増やす
        event.total_sold_tickets += 1
        event.resale_tickets -= 1
        event.save()

        # 購入完了ページにリダイレクト
        return redirect('re_pay_done_success', ticket_id=ticket.id)
    return HttpResponseBadRequest("無効なリクエストです。")


# 再販チケット用 成功メッセージ画面
@login_required
def re_pay_done_success(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # 合計金額を計算
    total_price = ticket.quantity * ticket.price

    return render(request, 'payment_success_resale.html', {
        'ticket': ticket,
        'total_price': total_price
    })







#再販処理（運営側）（いけ）
@login_required
def reticketcopy(request,post_id):
    # 元のオブジェクトを取得
    copyticket = Post.objects.get(pk=post_id)

    reticket = ReTicket(
        re_title=copyticket.event_name, #イベント名
        re_price=copyticket.price, #料金
        re_image=copyticket.image, #写真
        re_remaining_tickets=copyticket.remaining_tickets, #残りチケット枚数
        re_resale_tickets=copyticket.resale_tickets #再販チケット枚数
    )
    reticket.save()  # 新しいオブジェクトとして保存
    return render(request,'debug.html')

@csrf_exempt  # CSRF トークンのエラーを防ぐため
def submit_resale_ticket(request):
    if request.method == "POST":
        re_ticket_id = request.POST.get("re_ticket_id")
        result_date = request.POST.get("result_date")
        print(f"Received resale ticket ID: {re_ticket_id}, Result Date: {result_date}")
        return redirect("re_ticket")  # 申し込み後にリダイレクト

    return redirect("re_ticket")





#デバック
@login_required
def debug_view(request):
    return render(request, 'debug.html')

#ユーザー投稿機能
@login_required
def user_post_view(request):
    # 投稿をすべて取得（新しい順に並べる）
    posts = Post.objects.all().order_by('-id')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # フォームデータを保存
            return redirect('userpost')  # 投稿後にリダイレクト
    else:
        form = PostForm()
    return render(request, 'userpost.html', {'form': form, 'posts': posts})

def submit_post(request):
    if request.method == "POST":
        event_name = request.POST.get('event')
        comment = request.POST.get('comment')
        # コメントを保存
        Post.objects.create(event_name=event_name, comment=comment)
        return redirect('event')  # 投稿後にイベントページにリダイレクト

def event_page(request):
    posts = Post.objects.all()  # すべてのコメントを取得
    return render(request, 'event.html', {'posts': posts})

    
    
#利用者お問い合わせ

# # #お問い合わせ
# # 入力されたデータをDBに保存する関数(管理者)
# def connect_submit(request):
#     if request.method == 'POST':
#         form = ConnectForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "内容を送信しました。")
#             return redirect('connect')  # 送信後にリダイレクト
#         else:
#             messages.error(request, "フォームにエラーがあります。再度入力してください。")
#             return render(request, 'connect.html', {'form': form})  # エラー時に再度フォームを表示
#     else:
#         # CONNECT以外のリクエストは拒否
#         return redirect('connect')  # フォーム画面にリダイレクト

@login_required
def comment_list(request):
    form = CommentForm()  # フォームを作成

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # ログインユーザーをセット
            comment.save()
            return redirect('comment_list')

    context = {
        'seat_view_comments': Comment.objects.filter(category='seat_view'),
        'event_comments': Comment.objects.filter(category='event'),
        'transport_comments': Comment.objects.filter(category='transport'),
        'form': form,  # フォームをコンテキストに追加
    }
    return render(request, 'ticket_app/comment_list.html', context)

# #チケット再販購入
# @login_required
# def Reticket_menu(request):


# #データベースの内容をコピーする(後で使います)
# @login_required
# def test_connectcopy(request):
#     # 元のオブジェクトを取得
#     copyconnect = Connectreply.objects.get(pk=1)

#     # 複製を作成
#     copyconnect.pk = None  # プライマリキーをリセット
#     copyconnect.save()  # 新しいオブジェクトとして保存
#     return render(request,'policy.html')


#岸田の遺産
# #チケットキャンセル処理
# @login_required
# def cancel_ticket_view(request):
#     if request.method == 'POST':
#         ticket_id = request.POST.get('ticket_id')  # POSTされたチケットIDを取得
#         try:
#             # TicketHistoryから該当チケットを取得
#             ticket_history = TicketHistory.objects.get(id=ticket_id, user=request.user, status='pending')
            
#             # すでにキャンセルされている場合の処理
#             if ticket_history.status == 'canceled':
#                 return HttpResponse("このチケットは既にキャンセルされています。")
            
#             # キャンセル処理
#             ticket_history.status = 'canceled'
#             ticket_history.save()

#             # チケットの枚数を増加（キャンセルされた分、Postのチケット枚数を増やす）
#             post = ticket_history.event
#             post.number += 1  # 1枚分増加
#             post.save()

#             return redirect('cancel_done')  # キャンセル完了ページへリダイレクト

#         except TicketHistory.DoesNotExist:
#             return HttpResponse("指定されたチケットが見つかりません。")

#     elif request.method == 'GET':
#         # ユーザーがキャンセル可能なチケットを取得
#         tickets = TicketHistory.objects.filter(user=request.user, status='pending')
#         return render(request, 'CancelTicket.html', {'tickets': tickets})

#     else:
#         return HttpResponse("無効なリクエストです。")

