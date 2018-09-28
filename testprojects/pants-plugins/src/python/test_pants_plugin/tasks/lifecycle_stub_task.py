# coding=utf-8
# Copyright 2018 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import sys

from test_pants_plugin.subsystems.lifecycle_stubs import LifecycleStubs

from pants.base.exception_sink import ExceptionSink
from pants.base.exiter import Exiter
from pants.task.task import Task
from pants.util.memo import memoized_property


class MessagingExiter(Exiter):
  """An Exiter that prints a provided message to stderr."""

  def __init__(self, message):
    super(MessagingExiter, self).__init__()
    self._message = message

  def exit(self, *args, **kwargs):
    print(self._message, file=sys.stderr)
    super(MessagingExiter, self).exit(*args, **kwargs)


class LifecycleStubTask(Task):

  @classmethod
  def subsystem_dependencies(cls):
    return super(LifecycleStubTask, cls).subsystem_dependencies() + (LifecycleStubs.scoped(cls),)

  @memoized_property
  def _lifecycle_stubs(self):
    return LifecycleStubs.scoped_instance(self)

  def execute(self):
    exit_msg = self._lifecycle_stubs.add_exiter_message
    if exit_msg:
      new_exiter = MessagingExiter(exit_msg)
      ExceptionSink.reset_exiter(new_exiter)
    raise Exception('erroneous!')