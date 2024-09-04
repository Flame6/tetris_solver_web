from flask import Flask, render_template, request, url_for
import numpy as np

app = Flask(__name__)

# Define cases with updated abbreviations and their sizes
CASES = {
    'ammo': {'name': 'Ammunition Case', 'width': 2, 'height': 2},
    'cards': {'name': 'Keycard Holder Case', 'width': 1, 'height': 1},
    'docs': {'name': 'Documents Case', 'width': 2, 'height': 1},
    'food': {'name': 'Mr. Holodilnick Thermal Bag', 'width': 3, 'height': 3},
    'grenades': {'name': 'Grenade Case', 'width': 3, 'height': 3},
    'items': {'name': 'Item Case', 'width': 4, 'height': 4},
    'junk': {'name': 'Lucky Scav Junk Box', 'width': 4, 'height': 4},
    'keytool': {'name': 'Key Tool', 'width': 1, 'height': 1},
    'mags': {'name': 'Magazine Case', 'width': 3, 'height': 2},
    'medicine': {'name': 'Medicine Case', 'width': 3, 'height': 3},
    'money': {'name': 'Money Case', 'width': 3, 'height': 2},
    'pistol': {'name': 'Pistol Case', 'width': 2, 'height': 2},
    'sicc': {'name': 'S I C C Organizational Pouch', 'width': 2, 'height': 1},
    'stims': {'name': 'Injector Case', 'width': 1, 'height': 1},
    'tags': {'name': 'Dogtag Case', 'width': 1, 'height': 1},
    'THICCItems': {'name': 'T H I C C Item Case', 'width': 5, 'height': 3},
    'thiicweapons': {'name': 'T H I C C Weapon Case', 'width': 5, 'height': 2},
    'wallet': {'name': 'WZ Wallet', 'width': 1, 'height': 1},
    'weapons': {'name': 'Weapon Case', 'width': 5, 'height': 2}
}

def can_place(grid, block, x, y):
    """Check if a block can be placed at (x, y)"""
    for i in range(block['height']):
        for j in range(block['width']):
            if y + i >= grid.shape[0] or x + j >= grid.shape[1] or grid[y + i, x + j] != '.':
                return False
    return True

def place_block(grid, block, x, y, label):
    """Place a block on the grid"""
    for i in range(block['height']):
        for j in range(block['width']):
            grid[y + i, x + j] = label

def hybrid_solver(cases):
    grid_width = 10
    grid_height = 50
    grid = np.full((grid_height, grid_width), '.', dtype=str)

    placed_blocks = []

    for label, quantity in cases.items():
        block = CASES[label]
        for _ in range(quantity):
            placed = False
            for y in range(grid_height):
                for x in range(grid_width):
                    if can_place(grid, block, x, y):
                        place_block(grid, block, x, y, label)
                        placed_blocks.append({
                            'label': label,
                            'x': x,
                            'y': y,
                            'width': block['width'],
                            'height': block['height'],
                            'rotated': False
                        })
                        placed = True
                        break
                    rotated_block = {'width': block['height'], 'height': block['width']}
                    if can_place(grid, rotated_block, x, y):
                        place_block(grid, rotated_block, x, y, label)
                        placed_blocks.append({
                            'label': label,
                            'x': x,
                            'y': y,
                            'width': rotated_block['width'],
                            'height': rotated_block['height'],
                            'rotated': True
                        })
                        placed = True
                        break
                if placed:
                    break
    return grid, placed_blocks

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cases = {
            'ammo': int(request.form.get('ammo', 0)),
            'cards': int(request.form.get('cards', 0)),
            'docs': int(request.form.get('docs', 0)),
            'food': int(request.form.get('food', 0)),
            'grenades': int(request.form.get('grenades', 0)),
            'items': int(request.form.get('items', 0)),
            'junk': int(request.form.get('junk', 0)),
            'keytool': int(request.form.get('keytool', 0)),
            'mags': int(request.form.get('mags', 0)),
            'medicine': int(request.form.get('medicine', 0)),
            'money': int(request.form.get('money', 0)),
            'pistol': int(request.form.get('pistol', 0)),
            'sicc': int(request.form.get('sicc', 0)),
            'stims': int(request.form.get('stims', 0)),
            'tags': int(request.form.get('tags', 0)),
            'THICCItems': int(request.form.get('THICCItems', 0)),
            'thiicweapons': int(request.form.get('thiicweapons', 0)),
            'wallet': int(request.form.get('wallet', 0)),
            'weapons': int(request.form.get('weapons', 0)),
        }
        grid, placed_blocks = hybrid_solver(cases)

        return render_template('result.html', grid=grid, placed_blocks=placed_blocks, cases=CASES)

    return render_template('index.html', cases=CASES)

if __name__ == '__main__':
    app.run(debug=True)
