import logging


class SkipOptionsRequestsFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, "request") and record.request:
            record.request_ip = record.request.META.get("REMOTE_ADDR", "unknown")
            if record.request.method == "OPTIONS":
                return False
        return True
