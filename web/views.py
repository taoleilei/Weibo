from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from django.db.models import F
from web import models
# Create your views here.
from core.custom_queue import msgQueue
from Weibo import settings
from core.Backends import db_method
from core import redis_helper
import json
import time

# 用于检查用户是否登录
# @login_required


def index(request):
    # 访问首页
    # print('request.user.userprofile.id', request.user.userprofile.id)
    return render(request, 'Home/index.html', {'is_login': True})

# @csrf_protect


def create_wb(request):
    """创建、发布微博"""
    ret = {'status': True, 'data': ''}
    try:
        # 获取发过来的微博消息详细
        # {'data': {'viedo': '', 'content': '[em_28]hello python', 'time': 1474954943.9340596, 'wb_type': 0, 'topic': '', 'uid': ''}, 'status': True}
        data_str = request.POST.get('data', None)
        print(data_str)
        data_dict = json.loads(data_str)
        # 微博发布时间
        data_dict['time'] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())

        # 消息队列实例
        msg_queue = msgQueue()
        # 连接rabbitmq服务器
        msg_queue.make_conn()
        # 执行消息队列发布方法
        msg_queue.publish_wb(data_dict)

        # data_dict['time'] = time.strftime("%Y-%m-%d %X",time.localtime())
        ret['data'] = data_dict
        print(ret)
    except Exception as e:
        ret['status'] = False
        print('error', e)

    return HttpResponse(json.dumps(ret))


def get_new_wb_count(request):
    # 用户获取各自消息队列中新微博数量
    user_id = request.GET.get('user_id')
    msg_queue = msgQueue()
    msg_queue.make_conn()
    # 获取此用户队列类的新消息数
    count = msg_queue.get_new_wb_count("uid_%s" % (user_id,))
    print('count', count)
    return HttpResponse(json.dumps({'new_wb_count': count}))


def get_new_wb(request):
    # 用户获取各自队列中新的微博消息列表
    user_id = request.GET.get('user_id')
    msg_queue = msgQueue()
    msg_queue.make_conn()
    # 获取此用户队列内的新消息
    new_wb = msg_queue.get_new_wb("uid_%s" % (user_id,))
    # wb_id = new_wb['wb_id']
    # wb = models.Weibo.objects.filter(id__in[]).order_by('-id')
    return HttpResponse(json.dumps({'new_wb_list': new_wb}))


def upload_file(request):
    # 用户上传图片
    if request.method == 'POST':
        print(request.FILES)
        file_obj = request.FILES.get('file', None)
        print(file_obj)
        recv_size = 0
        # 服务端保存
        cache.delete(file_obj.name)
        # uid = request.user.userprofile.id
        uid = 1
        file_path = "%s/%s/temp/%s" % (settings.FILE_PATH, uid, file_obj.name)
        with open(file_path, 'wb+') as temp:
            for chunk in file_obj.chunks():
                temp.write(chunk)
                recv_size += len(chunk)
                cache.set(file_obj.name, recv_size)

        return HttpResponse(json.dumps({'status': True, 'filename': file_obj.name}))


def upload_file_progress(request):
    # 获取文件上传进度
    if request.method == 'GET':
        filename = request.GET.get('filename')
        upload_progress = cache.get(filename)
        return HttpResponse(json.dumps({'received_size': upload_progress}))
    else:
        cache_key = request.POST.get('cache_key')
        cache.delete(cache_key)
        return HttpResponse("cache key[%s] got deleted" % cache_key)


def favor(request):
    ret = {'status': True}
    try:
        wb_id = request.POST.get('wb_id')
        models.Weibo.objects.filter(id=wb_id).update(favor=F('favor') + 1)
    except Exception as e:
        ret['status'] = False
        print(e)
    return HttpResponse(json.dumps(ret))




@login_required
def home(request):
    # 个人主页
    return render(request, 'Home/home.html')


def search(request):
    # 搜索
    return render(request, 'Search/search.html')


def login_view(request):
    if request.method == "POST":
        post_data = request.POST.get('post_data', None)
        respons_status = {}

        if post_data:
            post_dic = json.loads(post_data)
            user_name = post_dic['user']
            passwd = post_dic['passwd']

            # 使用Django自带验证功能做验证
            # authenticate() 只是验证一个用户的证书而已。 而要登录一个用户，使用 login() 。
            user = authenticate(username=user_name, password=passwd)
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    # print("User is valid, active and authenticated")
                    # 存入uid,name到session
                    data = db_method.fetch_user_info_by_name(user_name)
                    request.session['uid'] = data['uid']
                    request.session['name'] = data['name']

                    # 放入活跃用户列表
                    re_helper = redis_helper.redis_helper()
                    re_helper.r.set(data['uid'], "RECENT_USER", ex=86400)
                    # print('[x] 活跃用户', re_helper.r.get(data['uid']))

                    # login()函数接受一个 HttpRequest 对象和一个 User 对象作为参数并使用Django的会话（
                    # session ）框架把用户的ID保存在该会话 中。
                    login(request, user)
                    respons_status['status'] = True
                    respons_status = json.dumps(respons_status)

                    # print("[auth]", request.user.is_authenticated)
                    return HttpResponse(respons_status)
                else:
                    print("The password is valid, but the account has been disabled!")
                    # pass
            else:
                # the authentication system was unable to verify the username and password
                # print("The username and password were incorrect.")
                respons_status['status'] = False
                respons_status[
                    'message'] = "The username and password were incorrect."
                respons_status = json.dumps(respons_status)
                return HttpResponse(respons_status)
        else:
            respons_status['status'] = False
            respons_status['message'] = "Invalid username and password."
            respons_status = json.dumps(respons_status)
            return HttpResponse(respons_status)

    else:
        # 有登录就给跳到index, 否则显示login页面
        if request.user.is_authenticated:
            print(" [x] start redirect to index... ")

            # return redirect('/index/')
            return render(request, 'Login/login.html')
        else:
            return render(request, 'Login/login.html')


def logout_view(request):
    if request.method == "GET":
        # 登出session
        logout(request)
        return redirect('/login/')
