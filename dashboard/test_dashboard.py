from django.contrib.auth.models import User
from django.test import TestCase

from dashboard.models import Group, Keyword, Document, InformationObject
from dashboard.models.category import GroupInfoObjectCategory


class BasicTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", password="test")
        self.group = Group.objects.create(administrator=self.user)
        self.category = GroupInfoObjectCategory.objects.create(title="Тестовая категория",
                                                               group=self.group)
        self.keywords = ["тесты", "unit", "tdd"]
        for word in self.keywords:
            kwd = Keyword(word=word, category=self.category)
            kwd.save()

    def test_get_keywords(self):
        """ Проверяем получение словаря ключевых слов """
        result = self.category.get_keywords()
        self.assertIsInstance(result, dict)
        self.assertEqual(set(self.keywords), set(result.keys()))

    def test_get_invite(self):
        """ Проверяем что приглашение в группу не пустое и содержит uuid """
        message = self.group.get_invite()
        self.assertIsInstance(message, str)
        self.assertGreater(message.__len__(), 0)
        self.assertTrue(message.find(str(self.group.group_uuid)) != -1)

    def test_get_first_message(self):
        """ Проверяем что первое сообщение не пустое и содержит uuid """
        message = self.group.get_invite()
        self.assertIsInstance(message, str)
        self.assertGreater(message.__len__(), 0)
        self.assertTrue(message.find(str(self.group.group_uuid)) != -1)


class DocumentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", password="test")
        self.group = Group.objects.create(administrator=self.user)
        self.category = GroupInfoObjectCategory.objects.create(title="Тестовая категория",
                                                               group=self.group)
        self.size = 3331113
        self.document = Document.objects.create(filename="Тестовый файл.txt",
                                                extension="txt",
                                                file_url="https://vk.com/doc141839173_545608039",
                                                size=self.size,
                                                source=InformationObject.Source.VK,
                                                connected_group=self.group,
                                                source_id=13132,
                                                category=self.category
                                                )

    def test_get_mb_size(self):
        bm_size = self.document.get_mb_size()
        self.assertGreater(bm_size, 1)
