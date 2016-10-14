# from core import custom_queue

# q = custom_queue.msgQueue()
# q.make_conn()
# weibo = q.get_new_wb('weibo')
# print(weibo.decode())
# # count = q.get_new_wb_count('weibo')
# # print(count)
# # weibo = q.get_new_wb('weibo')
# # print(weibo.decode())
# count = q.get_new_wb_count('weibo')
# print(count)
def application(env, start_response):
    start_response('200 OK',[('Content-Type','text/html')])
    return [b'hello world']