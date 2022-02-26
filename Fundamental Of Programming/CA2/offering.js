class Menu {
    constructor(type, code, name, price, option) {
        this.type = type
        this.code = code
        this.name = name
        this.price = price
        this.option = option
    }

    // Get all category from menuitems
    getCategory(){
        let categories = new Set()
        for (let item of MenuItems){
            categories.add(item.type)
        }
        return Array.from(categories)
    }

    // Get menu based on category
    getDish(category) {
        let dishes = []
        for (let item of MenuItems) {
            if (item.type == category) {
                dishes.push(item)
            }
        }
        return dishes
    }
}

let MenuItems = [
    new Menu("Appetizers", "a001", "Shrimp Scampi", "SGD 8.8", [["Spicy", "Non-spicy"]]),
    new Menu("Appetizers", "a002", "Chicken and Brie Quesadillas", "SGD 6.8", [["Spicy", "Non-spicy"]]),
    new Menu("Appetizers", "a003", "Fried Calamari", "SGD 5.8", [[]]),
    new Menu("Rice", "r001", "Mushroom Risotto", "SGD 8.8", [[]]),
    new Menu("Rice", "r002", "Seafood Paella", "SGD 12.8", [["Spicy", "Non-spicy"]]),
    new Menu("Rice", "r003", "Ham and Cheese baked rice", "SGD 8.4", [[]]),
    new Menu("Noodles", "n001", "Kimchi Udon", "SGD 7.9", [["Dry", "Soup"]]),
    new Menu("Noodles", "n002", "Sesame Soba", "SGD 6.8", [["Spicy", "Non-spicy"], ["Dry", "Soup"]]),
    new Menu("Noodles", "n003", "Chicken Ravioli", "SGD 11.7", [["Spicy", "Non-spicy"], ["Dry", "Soup"]]),
    new Menu("Drinks", "d001", "Virgin Piña Colada", "SGD 5.5", [[]]),
    new Menu("Drinks", "d001", "Strawberry Spritzer", "SGD 4.8", [[]]),
    new Menu("Drinks", "d003", "Calamansi Lime Juice", "SGD 4.2", [[]]),
]

module.exports = Menu;
