import unittest

import boto3
import psycopg2
import redis
import elasticsearch


class Test(unittest.TestCase):
    def test_redis(self):
        # Configure
        c = {
            'host': 'localhost',
            'port': 6379,
            'key': 'foo',
            'value': b'bar',
        }

        # Connect
        r = redis.Redis(host=c['host'], port=c['port'])

        # Set
        self.assertTrue(r.set(c['key'], c['value']))

        # Get
        self.assertEqual(r.get(c['key']), c['value'])

        # Delete
        self.assertGreater(r.delete(c['key']), 0)

    def test_postgres(self):
        # Configure
        c = {
            'host': 'localhost',
            'port': 5432,
            'user': 'postgres',
            'password': 'postgres',
            'database': 'postgres',
        }

        # Connect
        p = psycopg2.connect(
            host=c['host'],
            port=c['port'],
            user=c['user'],
            password=c['password'],
            database=c['database'],
        )

        # Status
        self.assertEqual(p.info.status, 0)

    def test_s3(self):
        # Configure
        c = {
            'host': 'localhost',
            'port': 9000,
            'access_key': 'minioadmin',
            'secret_key': 'minioadmin',
            'bucket_name': 'foo',
            'object_key': 'bar',
            'object_body': b'baz',
        }

        # Connect
        s3 = boto3.client(
            service_name='s3',
            aws_access_key_id=c['access_key'],
            aws_secret_access_key=c['secret_key'],
            endpoint_url=f'http://{c['host']}:{c['port']}',
        )

        # Create a bucket
        self.assertEqual(
            s3.create_bucket(
                Bucket=c['bucket_name']
            )['ResponseMetadata']['HTTPStatusCode'],
            200
        )

        # Put an object
        self.assertEqual(
            s3.put_object(
                Bucket=c['bucket_name'],
                Key=c['object_key'],
                Body=c['object_body']
            )['ResponseMetadata']['HTTPStatusCode'],
            200
        )

        # Get an object
        self.assertEqual(
            s3.get_object(
                Bucket=c['bucket_name'],
                Key=c['object_key']
            )['Body'].read(),
            c['object_body']
        )

        # Delete an object
        self.assertEqual(
            s3.delete_object(
                Bucket=c['bucket_name'],
                Key=c['object_key']
            )['ResponseMetadata']['HTTPStatusCode'],
            204
        )

        # Delete a bucket
        self.assertEqual(
            s3.delete_bucket(
                Bucket=c['bucket_name']
            )['ResponseMetadata']['HTTPStatusCode'],
            204
        )

    def test_elasticsearch(self):
        # Configure
        c = {
            'host': 'localhost',
            'port': 9200,
            'user': 'elastic',
            'password': 'elastic',
            'data': {
                'id': 1,
                'index': 'foo',
                'document': {
                    'content': 'python is the best language',
                },
                'query': {
                    'content': 'the best language',
                },
            },
        }

        # Connect
        es = elasticsearch.Elasticsearch(
            hosts=f'http://{c["host"]}:{c["port"]}',
            basic_auth=(c['user'], c['password']),
        )
        self.assertTrue(es.ping())

        # Index
        es.index(index=c['data']['index'], id=c['data']['id'], document=c['data']['document'])

        # Get
        self.assertEqual(
            es.get(index=c['data']['index'], id=c['data']['id'])['_source'],
            c['data']['document']
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
