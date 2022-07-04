from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from .forms import SearchForm
from .models import Checker, URL
from django.conf import settings

# django 내 유틸 함수들
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
# from django.utils import timezone

# Database
from django.db.models import Q
from django.db import connection

# 사용 모듈들
from bs4 import BeautifulSoup
import requests
import re


def MyURLClassifier(request):
    if request.method == 'POST':
        url_address = str(request.POST['url_address'])

        urls = URL.objects.all()

        if not url_address:
            object_list = Checker.objects.all()
            return render(request, 'checker/mychecker.html', {'object_list': object_list, 'urls': urls})

        object_list = Checker.objects.filter(url_address__exact=url_address)

        return render(request, 'checker/mychecker.html', {'object_list': object_list, 'urls': urls})


def URLClassifier(request):
    if request.method == 'POST':
        url_address = str(request.POST['url'])

        urls = Checker.objects.all()

        if not url_address:
            object_list = Checker.objects.all()
            return render(request, 'checker/checker_list.html', {'object_list': object_list, 'urls': urls})

        # object_list  Checker.objects.filter(available_display=True)
        object_list = Checker.objects.filter(url_address__exact=url_address)
        # current_category = get_object_or_404(Category, id=pk)
        # object_list = marks.filter(category=current_category)

        return render(request, 'checker/checker_list.html', {'object_list': object_list, 'urls': urls})


def MyChecker(request):
    object_list = Checker.objects.select_related('owner').all()
    urls = URL.objects.all()
    return render(request, "checker/mychecker.html", {'object_list': object_list, 'urls': urls})


class CheckerCreateView(CreateView):
    model = Checker
    fields = ['url_address']
    success_url = reverse_lazy('checker:mychecker')
    template_name_suffix = "_create"

    print("CheckerCreateView")

    def form_valid(self, form):
        if self.request.method == 'POST':
            form.instance.owner_id = self.request.user.id

            if form.is_valid():
                instance = form.save(commit=False)

                if not instance.url_address:
                    return self.render_to_response({'form': form})

                # url의 Response 정보를 저장
                url = str(instance.url_address)
                result = requests.get(url)

                instance.status_now = int(result.status_code)

                # Response 결과 페이지 저장
                result_page = result.content.decode('utf-8')
                instance.content_now = result_page

                # 이 부분 고치기
                instance.path = str(instance.url_address)

                # 시간 업데이트
                instance.last_checked = datetime.now()
                instance.save()

            return HttpResponseRedirect('/')


class CheckerListView(ListView):
    model = Checker
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        urls = URL.objects.all()
        object_list = Checker.objects.all()
        return render(request, 'checker/checker_list.html', {'object_list': object_list, 'urls': urls})


class CheckerDetailView(DetailView):
    model = Checker

    def checker_detail(request, id):
        object = get_object_or_404(Checker, id=id)
        return render(request, 'checker/checker_detail.html', {'object': object})


class CheckerUpdateView(UpdateView):
    model = Checker
    fields = ['url_address', 'memo', 'content_saved',
              'content_now', 'status_saved', 'status_now', 'page_excepted', 'fixed', 'vul_schedule']
    template_name_suffix = "_update"

    print("CheckerUpdateView")

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()

        if object.owner != request.user:
            # messages.warning(request, '수정 권한 없음')
            return HttpResponseRedirect('/')
        else:
            return super(CheckerUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print("form_valid")
        if self.request.method == 'POST':
            form.instance.owner_id = self.request.user.id

            if form.is_valid():
                print("CheckerUpdateView : form.is_valid 통과 1번")
                instance = form.save(commit=False)

                # object_list = checker.objects.filter(checker_slug__exact=form.instance.checker_slug).distinct()

                if not instance.content:
                    return self.render_to_response({'form': form})

                object_list = Checker.objects.all()

                # content 변경 시 update
                checker_content = object_list.values('content').get()
                content = str(checker_content['content_now'])

                if content != instance.content:
                    instance.content = content

                # last_checked 변경 시 update
                checker_last_checked = object_list.values('last_checked').get()
                last_checked = str(checker_last_checked['last_checked'])

                if last_checked != instance.last_checked:
                    instance.last_checked = last_checked

                # page_fixed 변경 시 update
                checker_page_fixed = object_list.values(
                    'fixed').get()
                page_fixed = str(checker_page_fixed['fixed'])

                if page_fixed != instance.page_fixed:
                    instance.page_fixed = page_fixed

                instance.save()

                return redirect('checker:checker_list')
            else:
                return self.render_to_response({'form': form})


class CheckerDeleteView(DeleteView):
    model = Checker
    success_url = reverse_lazy('checker:mychecker')

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.owner != request.user:
            # messages.warning(request, '삭제 권한 없음')
            return HttpResponseRedirect('/')
        else:
            return super(CheckerDeleteView, self).dispatch(request, *args, **kwargs)


class SearchFormView(FormView):
    form_class = SearchForm
    template_name = 'checker/search_result.html'

    def form_valid(self, form):
        # sql query string 테스트
        KeyWord = "%s" % self.request.POST['search_keyword']
        Checker_list = Checker.objects.filter(
            Q(checker_slug__icontains=KeyWord))

        context = {}
        context['form'] = form
        context['search_word'] = KeyWord
        context['Checker_list'] = Checker_list
        return render(self.request, self.template_name, context)


def Slug_in_URL(request, url_slug=None):
    current_url = None

    if url_slug:

        # 슬러그 처리
        object_list = Checker.objects.filter(
            checker_slug__exact=url_slug).distinct()

        checker_url = object_list.values('url').get()

        if checker_url['url']:
            current_url = checker_url['url']
        else:
            return render(request, 'checker/checker_notfound.html')

    count = object_list.values('count').get()
    object_list.update(count=count['count'] + 1)
    return render(request, 'checker/checker_redirect.html', {'current_url': current_url})
