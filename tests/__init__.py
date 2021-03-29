def assert_payload_field_type_value(obj, payload, field, data_type, value): 
    obj.assertIn(field, payload)
    obj.assertIsInstance(payload[field], data_type)
    obj.assertEqual(payload[field], value)


def assert_payload_field_type(obj, payload, field, data_type): 
    obj.assertIn(field, payload)
    obj.assertIsInstance(payload[field], data_type)
