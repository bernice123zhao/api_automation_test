from locust import HttpUser, task, constant, SequentialTaskSet


# 定义用户行为
class UserBehavior(SequentialTaskSet):
    def on_start(self):
        pass
    # @task(1)
    # def bky_index(self):
    #     self.client.get("/")
    @task
    def blogs_(self):
        head = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjhiODU5NWE1MTE3YTUyMjJiMzhhODhlZWRhODQwYjc3IiwidHlwIjoiSldUIn0.eyJuYmYiOjE1OTcwNDUxMDIsImV4cCI6MTU5NzEzMTUwMiwiaXNzIjoiaHR0cDovL3Nzby5xYS5jaGFuZ2luZ2VkdXN5cy5jb20iLCJhdWQiOlsiaHR0cDovL3Nzby5xYS5jaGFuZ2luZ2VkdXN5cy5jb20vcmVzb3VyY2VzIiwibWFzdGVyYXBpIiwicmV2ZW51ZUFwaSIsImNjQXBpIiwibWRBcGkiLCJpbnZBcGkiLCJ3ZkFwaSIsInBjQXBpIiwicGZBcGkiLCJvYUFwaSIsImhyQXBpIl0sImNsaWVudF9pZCI6Im9hIiwic3ViIjoiMDAwNTQ4NSIsImF1dGhfdGltZSI6MTU5NzA0NTEwMSwiaWRwIjoibG9jYWwiLCJuYW1lIjoi546L5p6X54eVIiwiZW1haWwiOiJ3YW5nbGlueWFuQGNoYW5naW5nZWR1LmNvbSIsIm9yZ0NvZGUiOiIwMTA0MDUwMiIsIm9yZ0lkIjoiMTMxNCIsImRlcGFydG1lbnQiOiLmlbDmja7kvpvnu5kiLCJwb3NpdGlvblRlbXBsYXRlIjoi5rWL6K-V5bel56iL5biIIiwicG9zaXRpb24iOiLmtYvor5Xlt6XnqIvluIgiLCJ1c2VyTm8iOiIwMDA1NDg1IiwidXNlcklkIjoiNDMyNCIsImlkQ2FyZCI6IjMyMDY4MyoqKioqKjExMDQyNyIsInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJtYXN0ZXJhcGkiLCJyZXZlbnVlQXBpIiwiY2NBcGkiLCJtZEFwaSIsImludkFwaSIsIndmQXBpIiwicGNBcGkiLCJwZkFwaSIsIm9hQXBpIiwiaHJBcGkiXSwiYW1yIjpbInB3ZCJdfQ.f3LRhFgkNlYfXPeKwk2_ajFqRmxKJR6S9gKaQL2ZlZ8JmzL0TH_sXbx3q8r6b2-WBBNoh2uWLz0MFXxGBVqakD4CMzlNSNNX6jb9dzgVlfGLWeB9-DLWcfyKZ1-slJrySWeqM0vlONXjuJQKgbTNP-NCjzr1VlAsmOt_NhJgsnugl0sDtsmZeGoXveKLOkRlGezxmYK6dTN9fDa0I5qWnfOcNYGbR0_ZQu6N74U9EQbFRD8BccOdS9sGJ0T94Ksz-qsq-2xsGRMixuEiFqkGVcgoD4BUewJc6F8Io__9z_2PkXAV3W5JqjwT7C6NE8_XLcO08JZkeLQVL_emfC8lew"}

        with self.client.get("/api/v2/AssetAllot/List", headers=head, catch_response=True) as resp:
            print(resp.content)
            # 如果响应状态码为 200，标记为成功
            if resp.status_code == 2001:
                resp.success()
            else:
                # 否则输出响应报文进一步排查
                resp.failure(resp.text)
    def on_stop(self):
        pass

class customUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = constant(5)
