#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys


class CustomException(Exception):
    def __init__(self, error_message, error_detail=None):
        super().__init__(error_message)

        exc_type, exc_value, exc_tb = sys.exc_info()

        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
        else:
            file_name = "Unknown"
            line_number = "Unknown"

        self.error_message = (
            f"Error in [{file_name}] at line [{line_number}]: {str(error_message)}"
        )

    def __str__(self):
        return self.error_message







