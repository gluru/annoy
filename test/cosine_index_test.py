from common import TestCase
from annoy import AnnoyIndex


class CosineIndexTest(TestCase):
    def test_get_distance(self):
        i = AnnoyIndex(4, 'cosine')
        i.add_item(0, [1, 0, 1, 1])
        i.add_item(1, [0, 1, 1, 0])
        i.add_item(2, [0, 0, 1, 0])
        i.add_item(3, [0, 0, 1, 1])
        i.add_item(4, [-1, 0, -1, -1])
        i.add_item(5, [0, 0, 0, 0])

        i.build(10)
        self.assertAlmostEqual(i.get_distance(0, 1), 0.295875)
        self.assertAlmostEqual(i.get_distance(0, 2), 0.211324)
        self.assertAlmostEqual(i.get_distance(0, 3), 0.091751)
        self.assertAlmostEqual(i.get_distance(0, 4), 1)
        self.assertAlmostEqual(i.get_distance(0, 5), 0.5)

    def test_get_ann_by_item(self):
        i = AnnoyIndex(4, 'cosine')
        i.add_item(0, [1, 0, 1, 1])
        i.add_item(1, [0, 1, 1, 0])
        i.add_item(2, [0, 0, 1, 0])
        i.add_item(3, [0, 0, 1, 1])
        i.build(10)

        items, distances = i.get_nns_by_item(0, n=3, include_distances=True)
        self.assertEqual(items[0], 0)
        self.assertEqual(items[1], 3)
        self.assertEqual(items[2], 2)
        self.assertAlmostEqual(distances[0], 0)
        self.assertAlmostEqual(distances[1], 0.091751)
        self.assertAlmostEqual(distances[2], 0.211324)

    def test_get_nns_by_vector(self):
        f = 3
        i = AnnoyIndex(f, 'cosine')
        i.add_item(0, [0, 0, 1])
        i.add_item(1, [0, 1, 0])
        i.add_item(2, [1, 0, 0])
        i.build(10)

        self.assertEqual(i.get_nns_by_vector([3, 2, 1], 3), [2, 1, 0])
        self.assertEqual(i.get_nns_by_vector([1, 2, 3], 3), [0, 1, 2])
        self.assertEqual(i.get_nns_by_vector([2, 0, 1], 3), [2, 0, 1])
