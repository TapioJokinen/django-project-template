from unittest import TestCase

from myapp.common.utils.converters import obj_to_camel_case, to_camel_case


class ConvertersTestCase(TestCase):
    def test_to_camel_case(self):
        snake_str_1 = "test_string"
        snake_str_2 = "teststring"
        snake_str_3 = "test_string_long_very_long"
        snake_str_4 = "test_STRING_long_AnD_wieRD"

        self.assertEqual(to_camel_case(snake_str_1), "testString")
        self.assertEqual(to_camel_case(snake_str_2), "teststring")
        self.assertEqual(to_camel_case(snake_str_3), "testStringLongVeryLong")
        self.assertEqual(to_camel_case(snake_str_4), "testStringLongAndWierd")

    def test_obj_to_camel_case(self):
        obj_1 = {
            "dog_dog": 1,
            "foobar": 1,
            "cat_cat": 1,
            "fish_fish": {"pike_pike": [1]},
        }
        obj_2 = [
            obj_1,
            {"moo_moo": obj_1},
            {
                "hello_hello": [
                    {"world_world": [{"duck_duck": obj_1}, {"duck_duck": obj_1}]},
                    {"world_world": [{"duck_duck": obj_1}, {"duck_duck": obj_1}]},
                ]
            },
        ]

        self.assertEqual(
            obj_to_camel_case(obj_1),
            {"dogDog": 1, "foobar": 1, "catCat": 1, "fishFish": {"pikePike": [1]}},
        )
        self.assertEqual(
            obj_to_camel_case(obj_2),
            [
                {"dogDog": 1, "foobar": 1, "catCat": 1, "fishFish": {"pikePike": [1]}},
                {
                    "mooMoo": {
                        "dogDog": 1,
                        "foobar": 1,
                        "catCat": 1,
                        "fishFish": {"pikePike": [1]},
                    }
                },
                {
                    "helloHello": [
                        {
                            "worldWorld": [
                                {
                                    "duckDuck": {
                                        "dogDog": 1,
                                        "foobar": 1,
                                        "catCat": 1,
                                        "fishFish": {"pikePike": [1]},
                                    }
                                },
                                {
                                    "duckDuck": {
                                        "dogDog": 1,
                                        "foobar": 1,
                                        "catCat": 1,
                                        "fishFish": {"pikePike": [1]},
                                    }
                                },
                            ]
                        },
                        {
                            "worldWorld": [
                                {
                                    "duckDuck": {
                                        "dogDog": 1,
                                        "foobar": 1,
                                        "catCat": 1,
                                        "fishFish": {"pikePike": [1]},
                                    }
                                },
                                {
                                    "duckDuck": {
                                        "dogDog": 1,
                                        "foobar": 1,
                                        "catCat": 1,
                                        "fishFish": {"pikePike": [1]},
                                    }
                                },
                            ]
                        },
                    ]
                },
            ],
        )
