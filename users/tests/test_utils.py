from datetime import date

from django.test import TestCase

from base.models import Purchase, Category
from family.models import Family, FamilyMember
from users.models import CustomUser

from users.utils import *
from users.utils import _get_day_month


class ProfileStatsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(name='testuser', username='testusername',
                                                   color='#7542f5', password='1234')
        self.family = Family.objects.create(name='testfamily')
        self.member = FamilyMember.objects.create(family=self.family, user=self.user)
        self.cat1 = Category.objects.create(name='testcategory1', family=self.family)
        self.cat2 = Category.objects.create(name='testcategory2', family=self.family)

    def last_month_date(self, date):
        month = date.month - 1
        if month <= 0:
            month = 12
        date = date.replace(day=1, month=month)
        return date

    def last_year_date(self, date):
        return date.replace(year=date.year - 1, day=1)

    def test_get_profile_empty_stats(self):
        purchase = Purchase.objects.all()
        stats = get_profile_stats(purchase)
        self.assertEqual(stats['user_sum'], 0)
        self.assertEqual(stats['user_month_sum'], 0)
        self.assertEqual(stats['user_month_cats'], 0)

    def test_get_profile_stats(self):
        Purchase.objects.create(name='1', user=self.user, family=self.family, category=self.cat1,
                                price=100, date=timezone.now().date())
        Purchase.objects.create(name='2', user=self.user, family=self.family, category=self.cat2,
                                price=100, date=timezone.now().date())
        purchase = Purchase.objects.all()
        stats = get_profile_stats(purchase)
        self.assertEqual(stats['user_sum'], 200)
        self.assertEqual(stats['user_month_sum'], 200)
        self.assertEqual(stats['user_month_cats'], 2)

    def test_get_another_month_stats(self):
        date = self.last_month_date(timezone.now())

        Purchase.objects.create(name='1', user=self.user, family=self.family, category=self.cat1,
                                price=100, date=date)
        purchase = Purchase.objects.all()
        stats = get_profile_stats(purchase)
        self.assertEqual(stats['user_sum'], 100)
        self.assertEqual(stats['user_month_sum'], 0)
        self.assertEqual(stats['user_month_cats'], 0)

    def test_get_mixed_month_stats(self):
        date = self.last_month_date(timezone.now())
        Purchase.objects.create(name='1', user=self.user, family=self.family, category=self.cat1,
                                price=100, date=date)
        Purchase.objects.create(name='2', user=self.user, family=self.family, category=self.cat2,
                                price=100, date=timezone.now().date())
        purchase = Purchase.objects.all()
        stats = get_profile_stats(purchase)
        self.assertEqual(stats['user_sum'], 200)
        self.assertEqual(stats['user_month_sum'], 100)
        self.assertEqual(stats['user_month_cats'], 1)

    def test_get_same_month_dif_year_stats(self):
        date = self.last_year_date(timezone.now())
        Purchase.objects.create(name='1', user=self.user, family=self.family, category=self.cat1,
                                price=100, date=date)
        Purchase.objects.create(name='2', user=self.user, family=self.family, category=self.cat2,
                                price=100, date=timezone.now().date())
        purchase = Purchase.objects.all()
        stats = get_profile_stats(purchase)
        self.assertEqual(stats['user_sum'], 200)
        self.assertEqual(stats['user_month_sum'], 100)
        self.assertEqual(stats['user_month_cats'], 1)


class ProfileStreakTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(name='testuser', username='testusername', color='#7542f5',
                                                   password='1234')
        self.family = Family.objects.create(name='testfamily')
        self.category = Category.objects.create(name='cat1', family=self.family)
        self.member = FamilyMember.objects.create(family=self.family, user=self.user)

    def test_empty_streak(self):
        purchases = Purchase.objects.all()
        self.assertEqual(get_streak(purchases), 0)

    def test_streak(self):
        for i in range(10):
            date = timezone.now().date() - timedelta(days=i)
            Purchase.objects.create(name='1', user=self.user, family=self.family, date=date,
                                    price=100, category=self.category)

        purchases = Purchase.objects.all()

        self.assertEqual(get_streak(purchases), 10)

    def test_streak_today_is_empty(self):
        for i in range(10):
            date = timezone.now().date() - timedelta(days=i + 1)
            Purchase.objects.create(name='1', user=self.user, family=self.family, date=date,
                                    price=100, category=self.category)

        purchases = Purchase.objects.all()

        self.assertEqual(get_streak(purchases), 10)

    def test_streak_two_days_is_empty(self):
        for i in range(10):
            date = timezone.now().date() - timedelta(days=i + 2)
            Purchase.objects.create(name='1', user=self.user, family=self.family, date=date,
                                    price=100, category=self.category)

        purchases = Purchase.objects.all()

        self.assertEqual(get_streak(purchases), 0)

    def test_streak_with_zero_day(self):
        for i in range(10):
            date = timezone.now().date() - timedelta(days=i)
            if i != 5:
                Purchase.objects.create(name='1', user=self.user, family=self.family, date=date,
                                        price=100, category=self.category)
        purchases = Purchase.objects.all()

        self.assertEqual(get_streak(purchases), 5)

    def test_streak_with_days_forward(self):
        for i in range(10):
            date = timezone.now().date() - timedelta(days=i - 2)
            Purchase.objects.create(name='1', user=self.user, family=self.family, date=date,
                                    price=100, category=self.category)
        purchases = Purchase.objects.all()

        self.assertEqual(get_streak(purchases), 8)

    def test_streak_only_one_day(self):
        Purchase.objects.create(name='1', user=self.user, family=self.family, date=timezone.now().date(),
                                price=100, category=self.category)
        purchases = Purchase.objects.all()
        self.assertEqual(get_streak(purchases), 1)

    def test_streak_with_couple_purchases_in_one_day(self):
        Purchase.objects.create(name='1', user=self.user, family=self.family, date=timezone.now().date(),
                                price=100, category=self.category)
        Purchase.objects.create(name='2', user=self.user, family=self.family, date=timezone.now().date(),
                                price=100, category=self.category)
        purchases = Purchase.objects.all()
        self.assertEqual(get_streak(purchases), 1)


class DayDotMonthConverterTestCase(TestCase):

    def test_empty_date(self):
        self.assertIsNone(_get_day_month(None))

    def test_day_month(self):
        self.assertEqual(_get_day_month(date(2026, 3, 2)), '02.03')

    def test_full_day_month(self):
        self.assertEqual(_get_day_month(date(2026, 3, 12)), '12.03')

    def test_day_full_month(self):
        self.assertEqual(_get_day_month(date(2026, 11, 2)), '02.11')

    def test_full_day_full_month(self):
        self.assertEqual(_get_day_month(date(2026, 11, 12)), '12.11')


class ActivityDaysTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(name='testuser', username='testusername', color='#7542f5',
                                                   password='1234')
        self.family = Family.objects.create(name='testfamily')
        self.category = Category.objects.create(name='cat1', family=self.family)
        self.member = FamilyMember.objects.create(family=self.family, user=self.user)

    def test_activity_day(self):
        today = timezone.now().date()
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=100, date=today)
        purchases = Purchase.objects.all()
        result = get_activity_days(purchases)
        self.assertEqual(result[_get_day_month(today)], 100)
        self.assertEqual(len(result), 30)

    def test_activity_days(self):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=100, date=today)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=200, date=yesterday)
        purchases = Purchase.objects.all()
        result = get_activity_days(purchases)
        self.assertEqual(result[_get_day_month(today)], 100)
        self.assertEqual(result[_get_day_month(yesterday)], 200)
        self.assertEqual(len(result), 30)

    def test_activity_days_month(self):
        today = timezone.now().date()
        yesterday = date(2026, 2, 27)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=100, date=today)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=200, date=yesterday)
        purchases = Purchase.objects.all()
        result = get_activity_days(purchases)
        self.assertEqual(result[_get_day_month(today)], 100)
        self.assertEqual(result[_get_day_month(yesterday)], 200)

    def test_empty_activity_days(self):
        purchases = Purchase.objects.all()
        result = get_activity_days(purchases)
        values = set(result.values())
        self.assertEqual(values, {0, })
        self.assertEqual(len(result), 30)

    def test_forward_activity_days(self):
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=100, date=today)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=200, date=tomorrow)
        purchases = Purchase.objects.all()
        result = get_activity_days(purchases)
        self.assertEqual(result[_get_day_month(today)], 100)
        self.assertFalse(_get_day_month(tomorrow) in result.keys())

    def test_activity_days_with_space(self):
        today = timezone.now().date()
        another_day = today - timedelta(days=2)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=100, date=today)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=200, date=another_day)
        purchases = Purchase.objects.all()
        result = get_activity_days(purchases)
        self.assertEqual(result[_get_day_month(today)], 100)
        self.assertEqual(result[_get_day_month(another_day)], 200)

    def test_border_activity_days(self):
        today = timezone.now().date()
        another_day = today - timedelta(days=29)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=100, date=today)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=200, date=another_day)
        purchases = Purchase.objects.all()
        result = get_activity_days(purchases)
        self.assertEqual(result[_get_day_month(today)], 100)
        self.assertEqual(result[_get_day_month(another_day)], 200)

    def test_above_border_activity_days(self):
        today = timezone.now().date()
        another_day = today - timedelta(days=30)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=100, date=today)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=200, date=another_day)
        purchases = Purchase.objects.all()
        result = get_activity_days(purchases)
        self.assertEqual(result[_get_day_month(today)], 100)
        self.assertFalse(_get_day_month(another_day) in result.keys())

    def test_couple_purchase_activity_day(self):
        today = timezone.now().date()
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=100, date=today)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category,
                                price=200, date=today)
        purchases = Purchase.objects.all()
        result = get_activity_days(purchases)
        self.assertEqual(result[_get_day_month(today)], 300)


class TopCategoryTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(name='testuser', username='testusername', color='#7542f5',
                                                   password='1234')
        self.family = Family.objects.create(name='testfamily')
        self.category1 = Category.objects.create(name='cat1', family=self.family)
        self.category2 = Category.objects.create(name='cat2', family=self.family)
        self.category3 = Category.objects.create(name='cat3', family=self.family)

        self.member = FamilyMember.objects.create(family=self.family, user=self.user)

    def test_empty_top(self):
        purchases = Purchase.objects.all()
        top = get_top_category(purchases)
        self.assertEqual(top, (None, None))

    def test_top_single_category(self):
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category1,
                                price=100, date=timezone.now().date())
        purchases = Purchase.objects.all()
        top = get_top_category(purchases)
        self.assertEqual(top, (self.category1, 100))

    def test_top_multiple_categories(self):
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category1,
                                price=100, date=timezone.now().date())
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category1,
                                price=100, date=timezone.now().date())
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category2,
                                price=100, date=timezone.now().date())
        purchases = Purchase.objects.all()
        top = get_top_category(purchases)
        self.assertEqual(top, (self.category1, 67))

    def test_top_two_equal_categories(self):
        Purchase.objects.create(name='test cat1', user=self.user, family=self.family, category=self.category1,
                                price=100, date=timezone.now().date())
        Purchase.objects.create(name='test cat2', user=self.user, family=self.family, category=self.category2,
                                price=100, date=timezone.now().date())
        purchases = Purchase.objects.all()
        top = get_top_category(purchases)
        self.assertEqual(top, (self.category1, 50))

    def test_top_three_equal_categories(self):
        Purchase.objects.create(name='test cat1', user=self.user, family=self.family, category=self.category1,
                                price=100, date=timezone.now().date())
        Purchase.objects.create(name='test cat2', user=self.user, family=self.family, category=self.category2,
                                price=100, date=timezone.now().date())
        Purchase.objects.create(name='test cat2', user=self.user, family=self.family, category=self.category3,
                                price=100, date=timezone.now().date())
        purchases = Purchase.objects.all()
        top = get_top_category(purchases)
        self.assertEqual(top, (self.category1, 33))

    def test_top_categories_with_diferent_year(self):
        today = timezone.now().date()
        year_ago = today.replace(year=today.year - 1)
        Purchase.objects.create(name='test cat1', user=self.user, family=self.family, category=self.category1,
                                price=100, date=today)
        Purchase.objects.create(name='test cat2', user=self.user, family=self.family, category=self.category2,
                                price=100, date=today)
        Purchase.objects.create(name='test cat1', user=self.user, family=self.family, category=self.category1,
                                price=100, date=year_ago)
        purchases = Purchase.objects.all()
        top = get_top_category(purchases)
        self.assertEqual(top, (self.category1, 50))

    def test_top_categories_with_different_month(self):
        today = timezone.now().date()
        month = today.month - 1
        if month == 0:
            month = 12
        month_ago = today.replace(month=month, day=1)
        Purchase.objects.create(name='test cat1', user=self.user, family=self.family, category=self.category1,
                                price=100, date=today)

        Purchase.objects.create(name='test cat2', user=self.user, family=self.family, category=self.category2,
                                price=100, date=month_ago)
        purchases = Purchase.objects.all()
        top = get_top_category(purchases)
        self.assertEqual(top, (self.category1, 100))

    def test_top_category_empty_current_month(self):
        today = timezone.now().date()
        month = today.month - 1
        if month == 0:
            month = 12
        month_ago = today.replace(month=month, day=1)
        Purchase.objects.create(name='test', user=self.user, family=self.family, category=self.category1,
                                price=100, date=month_ago)
        purchases = Purchase.objects.all()
        top = get_top_category(purchases)
        self.assertEqual(top, (None, None))
