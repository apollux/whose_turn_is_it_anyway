# -*- coding: utf-8 -*-
import pytest

from whose_turn_is_it_anyway.public.forms import LoginForm
from whose_turn_is_it_anyway.user.forms import RegisterForm
from .factories import UserFactory


class TestRegisterForm:

    def test_validate_user_already_registered(self, user):
        # Enters username that is already registered
        form = RegisterForm(username=user.username, email='foo@bar.com',
            password='example', confirm='example')

        assert form.validate() is False
        assert 'Username already registered' in form.username.errors

    def test_validate_email_already_registered(self, user):
        # enters email that is already registered
        form = RegisterForm(username='unique', email=user.email,
            password='example', confirm='example')

        assert form.validate() is False
        assert 'Email already registered' in form.email.errors

    def test_validate_success(self, db):
        form = RegisterForm(username='newusername', email='new@test.test',
            password='example', confirm='example')
        assert form.validate() is True


class TestLoginForm:

    def test_validate_success(self, user):
        user.set_password('example')
        user.save()
        form = LoginForm(username=user.username, password='example')
        assert form.validate() is True
        assert form.user == user

    def test_validate_unknown_username(self, db):
        form = LoginForm(username='unknown', password='example')
        assert form.validate() is False
        assert 'Invalid username and password combination' in form.username.errors
        assert form.user is None

    def test_validate_invalid_password(self, user):
        user.set_password('example')
        user.save()
        form = LoginForm(username=user.username, password='wrongpassword')
        assert form.validate() is False
        assert 'Invalid username and password combination' in form.username.errors

    def test_validate_inactive_user(self, user):
        user.active = False
        user.set_password('example')
        user.save()
        # Correct username and password, but user is not activated
        form = LoginForm(username=user.username, password='example')
        assert form.validate() is False
        assert 'User not activated' in form.username.errors
