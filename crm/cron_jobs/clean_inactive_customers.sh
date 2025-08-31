#!/bin/bash

# Run Django shell command to delete inactive customers
deleted_count=$(python manage.py shell -c "
import datetime
from crm.models import Customer, Order

one_year_ago = datetime.date.today() - datetime.timedelta(days=365)

inactive_customers = Customer.objects.exclude(
    id__in=Order.objects.filter(order_date__gte=one_year_ago).values_list('customer_id', flat=True)
)

count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log result with timestamp
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo \"$timestamp - Deleted $deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
