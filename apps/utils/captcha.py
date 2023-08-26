import re

from application.settings import REGEX_MOBILE
from apps.utils.json_response import DetailResponse
from apps.utils.viewset import CustomModelViewSet
from random import choice
from rest_framework.request import Request
from rest_framework import exceptions


