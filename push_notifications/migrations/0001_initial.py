from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # Lista de dependências de outras migrações, se houver
    ]

    operations = [
        # Lista de operações a serem executadas durante a migração
    ]


# from django.db import migrations

# def create_notifications(apps, schema_editor):
#     #apps.get_model('push_notifications', 'Notification')
#     default_notifications = [
#         {
#             'icon': 'documents-outline',
#             'title': 'Análise documental',
#             'message': 'Seus documentos se encontram em análise pela engenharia ambiental. Em breve entraremos em contato!',
#         },
#         {
#             'icon': 'wallet-outline',
#             'title': 'Viabilidade econômica',
#             'message': 'Estamos realizando a análise de viabilidade econômica e retorno financeiro da sua propriedade. Em breve entraremos em contato!'
#         },
#         {
#             'icon': 'leaf-outline',
#             'title': 'Projeto de carbono',
#             'message': 'Nossa equipe de engenheiros está desenvolvendo seu projeto de geração de créditos de carbono. Em breve entraremos em contato!'
#         },
#         {
#             'icon': 'checkmark-circle-outline',
#             'title': 'Validação e certificação',
#             'message': 'Seu projeto de geração de créditos de carbono se encontra em análise pela certificadora e pela validadora. Em breve entraremos em contato!'
#         },
#         {
#             'icon': 'trending-up-outline',
#             'title': 'Geração de créditos de carbono',
#             'message': 'Seus documentos se encontram em análise pela engenharia ambiental. Em breve entraremos em contato!'
#         },
#     ]
#     for notification_data in default_notifications:
#         Notification.objects.create(**notification_data)

# class Migration(migrations.Migration):


#     operations = [
#         migrations.RunPython(create_notifications),
#     ]
