#!/usr/bin/python
# coding: utf-8
from locust import HttpLocust, TaskSet, task


class TestLoadTests(TaskSet):
    def on_start(self):
        print "On start"

    @task
    def test_vote(self):
        vote = {
            'wall': 1,
            'vote': 3,
        }
        csrf_token = self.client.get('').cookies['csrftoken']
        self.client.post('/voting', vote, headers={"X-CSRFToken": csrf_token})


class WebsiteUser(HttpLocust):
    host = 'http://localhost'
    task_set = TestLoadTests
