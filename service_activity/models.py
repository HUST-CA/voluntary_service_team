from django.db import models


class Member(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=16)
    tel = models.CharField(verbose_name='电话', max_length=11)
    sex = models.CharField(verbose_name='性别', max_length=16, choices=(('男', '男'), ('女', '女')))
    email = models.EmailField(verbose_name='邮箱', max_length=64, blank=True)
    college = models.CharField(verbose_name='学院-年级', max_length=64, blank=True)
    info = models.TextField(verbose_name='其他', blank=True)

    def involved_activities(self):
        return self.activities

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '成员'
        verbose_name_plural = '成员'


class ServiceActivityManager(models.Manager):
    def count_activities(self):
        '''返回一共有多少次活动'''
        return len(self.get_queryset())

    def recent_activity(self):
        '''返回最近一次的活动'''
        return self.get_queryset().filter(int_id=self.count_activities())[0]
        # 测试环境下可能会有多个返回结果,故不使用get

    def recent_activity_date(self):
        '''返回最近一次的活动日期'''
        return self.recent_activity().activity_date


class ServiceActivity(models.Model):
    # date_tuple = datetime.date.today().timetuple()
    activity_date = models.DateField(verbose_name='活动日期', auto_now_add=True)
    place = models.CharField(verbose_name='地点', max_length=128)
    FLAGS = (('进行中', '进行中'), ('已完成', '已完成'))
    flag = models.CharField(verbose_name='状态', max_length=16, choices=FLAGS)
    int_id = models.IntegerField(verbose_name='第几次活动')  # this should be filled when it's created

    members = models.ManyToManyField(Member, related_name='activities', verbose_name='成员', blank=True)

    objects = ServiceActivityManager

    def __str__(self):
        return self.activity_time + '于' + self.place
