from task_engine.enums.task_status import TaskStatus
from task_engine.core.registry import Registry
import re

def OnSuccess(task_name: str):
    def _condition(ctx):
        return ctx.task_states.get(task_name) == TaskStatus.SUCCESS
    return _condition

def OnFailed(task_name: str):
    def _condition(ctx):
        return ctx.task_states.get(task_name) == TaskStatus.FAILED
    return _condition

def OnSkipped(task_name: str):
    def _condition(ctx):
        return ctx.task_states.get(task_name) == TaskStatus.SKIPPED
    return _condition

def Env(key: str, value=None):
    def _condition(ctx):
        env_value = ctx.env.get(key)
        if value is None:
            return bool(env_value)
        return env_value == value
    return _condition

def OnExceptionType(task_name: str, exc_type: type[Exception]):
    def _condition(ctx):
        error = ctx.task_errors.get(task_name)
        if not error:
            return False
        return issubclass(error.get_error_type(), exc_type)
    return _condition