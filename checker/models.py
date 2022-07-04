from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class URL(models.Model):
    url = models.CharField(max_length=200, unique=True, blank=False)

    class Meta:
        verbose_name = 'url'
        verbose_name_plural = 'urls'

    def __str__(self):
        return str(self.url)


class Checker(models.Model):
    sn = models.AutoField(
        primary_key=True, unique=True, editable=False, verbose_name='ID')
    url_address = models.ForeignKey(
        URL, on_delete=models.CASCADE, related_name='checker')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_checkers")
    path = models.CharField(blank=False, max_length=300)
    memo = models.TextField(blank=True)

    # HTTP Body Response
    content_saved = models.TextField(blank=True)
    content_now = models.TextField(blank=True)
    status_saved = models.PositiveSmallIntegerField(blank=False, default=200)
    status_now = models.PositiveSmallIntegerField(blank=False, default=200)

    page_excepted = models.BooleanField('excepted', default=False)  # 페이지 예외 처리
    last_checked = models.DateTimeField(
        auto_now=True, blank=True)      # 최근 확인 시간
    fixed = models.BooleanField(default=False)      # 취약점 수정 여부
    vul_schedule = models.PositiveSmallIntegerField(blank=False, default=0)

    # class Meta:
    #     ordering = ['checker_slug']

    def __str__(self):
        return str(self.url_address)

    def get_absolute_url(self):
        return reverse("detail", args=[self.id])


class ScanMode(models.Model):
    scan_mode = models.PositiveSmallIntegerField(
        blank=False, default=1)  # 1: Normal, 2: A3C, 3: Hybrid

    class Meta:
        verbose_name = 'scan_mode'
        verbose_name_plural = 'scan_modes'

    def __str__(self):
        return str(self.scan_mode)
