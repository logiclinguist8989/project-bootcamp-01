from . import models

# Reward rules
STAR_PER_LETTER = 1
STICKER_EVERY = 5  # every 5 letters completed -> sticker
BADGE_THRESHOLD = 20  # award badge when >= 20 letters


def process_progress(letter, correct, user_id=1):
    """Handle reward logic after a letter play.
    Returns a dict with updated progress row and any rewards granted.
    """
    # fetch existing state
    before = {r['letter']: r for r in models.get_letters(user_id)}
    old = before.get(letter)
    was_completed = bool(old and old['completed'])

    # update progress row
    new_row = models.update_letter_progress(letter, correct, user_id)

    rewards_granted = {"stars": 0, "stickers": [], "badges": []}

    if correct and not was_completed:
        # award stars
        models.add_stars(STAR_PER_LETTER, user_id)
        rewards_granted['stars'] += STAR_PER_LETTER

        # count completed letters
        letters = models.get_letters(user_id)
        completed_count = sum(1 for l in letters if l['completed'])

        # sticker logic
        if completed_count % STICKER_EVERY == 0:
            sticker_code = f"sticker_{completed_count}"
            models.add_sticker(sticker_code, user_id)
            rewards_granted['stickers'].append(sticker_code)

        # badge logic
        if completed_count >= BADGE_THRESHOLD:
            badge_code = 'super_reader'
            models.set_badge(badge_code, user_id)
            rewards_granted['badges'].append(badge_code)

    # return updated rewards and row
    rewards = models.get_rewards(user_id)
    return {"progress": new_row, "rewards": rewards, "granted": rewards_granted}
