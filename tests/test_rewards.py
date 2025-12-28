import unittest
from backend import models, rewards

class TestRewards(unittest.TestCase):
    def setUp(self):
        models.init_db()

    def test_award_star_on_first_complete(self):
        # reset rewards
        models.init_db()
        models.reset_rewards()
        before = models.get_rewards()['stars']
        res = rewards.process_progress('Z', True)
        after = models.get_rewards()['stars']
        self.assertEqual(after, before + 1)

    def test_no_duplicate_star_when_already_completed(self):
        models.init_db()
        models.reset_rewards()
        # complete A twice
        rewards.process_progress('A', True)
        before = models.get_rewards()['stars']
        rewards.process_progress('A', True)
        after = models.get_rewards()['stars']
        self.assertEqual(after, before)

if __name__ == '__main__':
    unittest.main()
