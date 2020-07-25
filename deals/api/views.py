import csv
import io
from django.db.models import Sum
from django.db.models.query import QuerySet
from items.models import Item
from .serializers import DealSerializer, TopUsersSerializers
from django.contrib.auth.models import User
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response


class Top5List(mixins.ListModelMixin,
               generics.GenericAPIView):
    serializer_class = TopUsersSerializers
    queryset = User.objects.all()

    def get_queryset(self):
        customers_pool = User.objects.annotate(total_spent=Sum('deals__total')).order_by('-total_spent')
        data = []
        if User.objects.count() >= 4:
            top5 = customers_pool.exclude(total_spent__lt=customers_pool[4].total_spent)
            for customer in top5:
                other_customers = top5.exclude(username=customer.username)
                gems = Item.objects.filter(id__in=customer.deals.values('item')).distinct()
                popular_gems = gems.filter(deals__customer__in=other_customers)
                info = {
                    "username": customer.username,
                    "total_spent": customer.total_spent,
                    "gems": popular_gems
                }
                data.append(info)
        queryset = data
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UploadCSV(APIView):
    def post(self, request, format=None):
        errors = []
        flag = True
        csv_file = request.FILES['deals']
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            User.objects.get_or_create(username=column[0])
            Item.objects.get_or_create(name=column[1])
            data = {}
            try:
                data = {'customer': User.objects.get(username=column[0]).pk,
                        'item': Item.objects.get(name=column[1]).pk,
                        'total': column[2],
                        'quantity': column[3],
                        'date': column[4]}
            except:
                flag = False
                errors.append(column)
            serializer = DealSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                flag = False
        if flag:
            return Response('OK - файл был обработан без ошибок', status=status.HTTP_201_CREATED)
        return Response('В процессе обработки файла произошла ошибка в следующих строках' + str(errors),
                        status=status.HTTP_400_BAD_REQUEST)
