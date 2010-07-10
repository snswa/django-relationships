from django.dispatch import Signal

relationship_added = Signal(providing_args=["instance", "from_user", "to_user", "status"])

relationship_removed = Signal(providing_args=["instance", "from_user", "to_user", "status"])
