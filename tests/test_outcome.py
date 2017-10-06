from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.account import Account
from canvasapi.course import Course
from canvasapi.outcome import Outcome, OutcomeGroup, OutcomeLink
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestOutcome(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    'course': ['get_by_id'],
                    'outcome': [
                        'account_root_outcome_group',
                        'canvas_root_outcome_group',
                        'course_root_outcome_group',
                        'course_outcome_links_in_context',
                        'outcome_example'
                    ]
                }, m
            )

            self.course = self.canvas.get_course(1)
            self.course_outcome_links = self.course.get_all_outcome_links_in_context()
            self.example_outcome = self.course_outcome_links[0].get_outcome()

    # __str__()
    def test__str__(self, m):
        string = str(self.example_outcome)
        self.assertIsInstance(string, str)

    # show()
    def test_show(self, m):
        register_uris({'outcome': ['outcome_show']}, m)
        test_show = self.example_outcome.show()
        self.assertIsInstance(test_show, Outcome)

    # update()
    def test_update(self, m):
        register_uris({'outcome': ['outcome_update']}, m)
        self.assertEqual(self.example_outcome.title, 'Outcome Show Example')
        result = self.example_outcome.update(title="new_title")
        self.assertTrue(result)
        self.assertIsInstance(self.example_outcome, Outcome)
        self.assertEqual(self.example_outcome.title, "new_title")


@requests_mock.Mocker()
class TestOutcomeLink(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    'course': ['get_by_id'],
                    'outcome': [
                        'course_root_outcome_group',
                        'course_outcome_links_in_context'
                    ]
                }, m
            )

            self.course = self.canvas.get_course(1)
            self.course_outcome_links = self.course.get_all_outcome_links_in_context()

    # __str__()
    def test__str__(self, m):
        register_uris({'outcome': ['course_outcome_links_in_context']}, m)
        string = str(self.course_outcome_links[0])
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestOutcomeGroup(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    'account': ['get_by_id'],
                    'course': ['get_by_id'],
                    'outcome': [
                        'account_root_outcome_group',
                        'canvas_root_outcome_group',
                        'course_root_outcome_group',
                        'course_outcome_links_in_context',
                        'outcome_example'
                    ]
                }, m
            )

            self.canvas_outcome_group = self.canvas.get_root_outcome_group()

            self.account = self.canvas.get_account(1)
            self.account_outcome_group = self.account.get_root_outcome_group()
            self.account_outcome_groups = self.account.get_outcome_groups_in_context()
            self.account_outcome_links = self.account.get_all_outcome_links_in_context()

            self.course = self.canvas.get_course(1)
            self.course_outcome_group = self.course.get_root_outcome_group()
            self.course_outcome_groups = self.course.get_outcome_groups_in_context()
            self.course_outcome_links = self.course.get_all_outcome_links_in_context()

            self.example_outcome = self.course_outcome_links[0].get_outcome()

    # __str__()
    def test__str__(self, m):
        string = str(self.canvas_outcome_group)
        self.assertIsInstance(string, str)

    # show()
    def test_show(self, m):
        register_uris(
            {
                'outcome': [
                    'outcome_group_show_global',
                    'outcome_group_show_account',
                    'outcome_group_show_course'
                ]
            }, m)
        test_show_outcome_group = self.account_outcome_group.show()
        self.assertIsInstance(test_show_outcome_group, OutcomeGroup)
        self.assertEqual(test_show_outcome_group.context_type, 'Account')
        test_show_outcome_group = self.canvas_outcome_group.show()
        self.assertIsInstance(test_show_outcome_group, OutcomeGroup)
        test_show_outcome_group = self.course_outcome_group.show()
        self.assertIsInstance(test_show_outcome_group, OutcomeGroup)

    # update()
    def test_update(self, m):
        register_uris(
            {
                'outcome': [
                    'outcome_group_update_global',
                    'outcome_group_update_account',
                    'outcome_group_update_course'
                ]
            }, m)

        new_title = "New Outcome Group Title"

        self.assertEqual(self.account_outcome_group.title, 'ROOT')
        result = self.account_outcome_group.update(title=new_title)
        self.assertTrue(result)
        self.assertIsInstance(self.account_outcome_group, OutcomeGroup)
        self.assertEqual(self.account_outcome_group.title, new_title)

        self.assertEqual(self.canvas_outcome_group.title, 'ROOT')
        result = self.canvas_outcome_group.update(title=new_title)
        self.assertTrue(result)
        self.assertIsInstance(self.canvas_outcome_group, OutcomeGroup)
        self.assertEqual(self.canvas_outcome_group.title, new_title)

        self.assertEqual(self.course_outcome_group.title, 'ROOT')
        result = self.course_outcome_group.update(title=new_title)
        self.assertTrue(result)
        self.assertIsInstance(self.course_outcome_group, OutcomeGroup)
        self.assertEqual(self.course_outcome_group.title, new_title)

    # delete()
    def test_delete(self, m):
        register_uris(
            {
                'outcome': [
                    'outcome_group_delete_global',
                    'outcome_group_delete_account',
                    'outcome_group_delete_course'
                ]
            }, m)

        self.assertEqual(self.account_outcome_group.title, 'ROOT')
        result = self.account_outcome_group.delete()
        self.assertTrue(result)

        self.assertEqual(self.canvas_outcome_group.title, 'ROOT')
        result = self.canvas_outcome_group.delete()
        self.assertTrue(result)

        self.assertEqual(self.course_outcome_group.title, 'ROOT')
        result = self.course_outcome_group.delete()
        self.assertTrue(result)

    # list_linked_outcomes()
    def test_list_linked_outcomes(self, m):
        register_uris(
            {
                'outcome': [
                    'outcome_group_list_linked_outcomes_account',
                    'outcome_group_list_linked_outcomes_global',
                    'outcome_group_list_linked_outcomes_courses'
                ]
            }, m)

        result = self.account_outcome_group.list_linked_outcomes()
        self.assertIsInstance(result[0], OutcomeLink)
        self.assertEqual(result[0].outcome_group['id'], 2)
        self.assertEqual(result[0].outcome_group['title'], "Account Test Outcome Group")

        result = self.canvas_outcome_group.list_linked_outcomes()
        self.assertIsInstance(result[0], OutcomeLink)
        self.assertEqual(result[0].outcome_group['id'], 2)
        self.assertEqual(result[0].outcome_group['title'], "Global Test Outcome Group")

        result = self.course_outcome_group.list_linked_outcomes()
        self.assertIsInstance(result[0], OutcomeLink)
        self.assertEqual(result[0].outcome_group['id'], 2)
        self.assertEqual(result[0].outcome_group['title'], "Course Test Outcome Group")

    # link_existing()
    def test_link_existing(self, m):
        register_uris(
            {
                'outcome': [
                    'outcome_example',
                    'outcome_group_link_existing_global',
                    'outcome_group_link_existing_account',
                    'outcome_group_link_existing_course'
                ]
            }, m)

        result = self.canvas_outcome_group.link_existing(self.example_outcome)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group['id'], 2)

        result = self.account_outcome_group.link_existing(self.example_outcome)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group['id'], 2)

        result = self.course_outcome_group.link_existing(self.example_outcome)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group['id'], 2)

        result = self.canvas_outcome_group.link_existing(3)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group['id'], 2)

        result = self.account_outcome_group.link_existing(3)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group['id'], 2)

        result = self.course_outcome_group.link_existing(3)
        self.assertIsInstance(result, OutcomeLink)
        self.assertEqual(result.outcome_group['id'], 2)

    '''
    # link_new()
    def test_link_new(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeLink)
    '''

    '''
    # unlink_outcome()
    def test_unlink_outcome(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeLink)
    '''

    '''
    # list_subgroups()
    def test_list_subgroups(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ[0], OutcomeGroup)
    '''

    '''
    # create_subgroup()
    def test_create_subgroup(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeGroup)
    '''

    '''
    # import_outcome_group()
    def test_import_outcome_group(self, m):
        TEST_OBJ = "replace this"

        self.assertIsInstance(TEST_OBJ, OutcomeGroup)
    '''
