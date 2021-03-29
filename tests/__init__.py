def assert_payload_field_type_value(obj, payload, field, data_type, value): 
    obj.assertIn(field, payload)
    obj.assertIsInstance(payload[field], data_type)
    obj.assertEqual(value, payload[field])


def assert_payload_field_type(obj, payload, field, data_type): 
    obj.assertIn(field, payload)
    obj.assertIsInstance(payload[field], data_type)
