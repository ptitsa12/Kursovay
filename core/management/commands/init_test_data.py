from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from employees.models import Employee
from suppliers.models import Supplier
from catalog.models import Product
from procurement.models import PurchaseRequest, SupplierOrder, Invoice


class Command(BaseCommand):
    help = 'Идемпотентная загрузка тестовых данных'

    GROUPS = ['storekeeper', 'purchaser', 'accountant', 'manager']

    def handle(self, *args, **options):
        self._create_groups()
        self._create_admin()
        users = self._create_role_users()
        suppliers = self._create_suppliers()
        products = self._create_products()
        self._create_demo_flow(users, suppliers, products)
        self.stdout.write(self.style.SUCCESS('Тестовые данные готовы'))

    def _create_groups(self):
        for name in self.GROUPS:
            Group.objects.get_or_create(name=name)

    def _create_admin(self):
        if not Employee.objects.filter(username='admin').exists():
            Employee.objects.create_superuser(
                username='admin',
                password='admin123',
                email='admin@example.com',
                first_name='Админ',
                last_name='Системный',
                position='Администратор',
                department='ИТ',
            )
            self.stdout.write('Создан admin / admin123')

    def _create_role_users(self):
        roles = {
            'storekeeper': ('storekeeper', 'Иван', 'Кладов', 'Кладовщик', 'Склад'),
            'purchaser': ('purchaser', 'Пётр', 'Закуп', 'Закупщик', 'Снабжение'),
            'accountant': ('accountant', 'Анна', 'Бух', 'Бухгалтер', 'Финансы'),
            'manager': ('manager', 'Сергей', 'Рук', 'Руководитель', 'Управление'),
        }
        users = {}
        for username, (group, first, last, pos, dept) in roles.items():
            user, created = Employee.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'position': pos,
                    'department': dept,
                    'email': f'{username}@example.com',
                },
            )
            if created:
                user.set_password('testpass123')
                user.save()
            group_obj = Group.objects.get(name=group)
            user.groups.add(group_obj)
            users[username] = user
        return users

    def _create_suppliers(self):
        data = [
            ('ООО ТехСнаб', '7701000001', '5.00', True),
            ('ООО ДетальПром', '7701000002', '4.20', True),
            ('ООО НизРейтинг', '7701000003', '2.50', True),
        ]
        suppliers = []
        for name, inn, rating, active in data:
            s, _ = Supplier.objects.get_or_create(
                inn=inn,
                defaults={
                    'name': name,
                    'contact_phone': '+79000000000',
                    'email': f'{inn}@supplier.ru',
                    'rating': Decimal(rating),
                    'is_active': active,
                },
            )
            suppliers.append(s)
        return suppliers

    def _create_products(self):
        products = []
        for i in range(1, 6):
            p, _ = Product.objects.get_or_create(
                sku=f'SKU-{i:03d}',
                defaults={
                    'name': f'Деталь {i}',
                    'unit': 'шт',
                    'cost_code': f'CC-{i}',
                },
            )
            products.append(p)
        return products

    def _create_demo_flow(self, users, suppliers, products):
        storekeeper = users['storekeeper']
        purchaser = users['purchaser']
        good_supplier = suppliers[0]

        req, created = PurchaseRequest.objects.get_or_create(
            product=products[0],
            created_by=storekeeper,
            defaults={
                'quantity': 10,
                'desired_date': date.today() + timedelta(days=14),
                'status': 'accepted',
            },
        )
        if created:
            self.stdout.write(f'Создана заявка #{req.id}')

        order, o_created = SupplierOrder.objects.get_or_create(
            request=req,
            defaults={
                'supplier': good_supplier,
                'amount': Decimal('15000.00'),
                'status': 'sent',
            },
        )
        if o_created:
            self.stdout.write(f'Создан заказ {order.order_number}')

        Invoice.objects.get_or_create(
            order=order,
            invoice_number='INV-DEMO-001',
            defaults={'document_date': date.today()},
        )
