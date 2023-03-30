const input = require('readline-sync');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');

const Menu = require('./offering');
const Cart = require('./OrderCart');

function question(select) {
    switch (select) {
        case `Start`:
            console.clear()
            for (qns of consoleQuestions.Start) { console.log(qns) }
            switch (input.questionInt(">>>>")) {
                case 1:
                    console.clear()
                    showMenu()
                    break
                case 2:
                    console.clear()
                    showCart()
                    break
                case 0:
                    console.clear()
                    question(`Quit`)
                default:
                    console.clear()
                    question(`Start`)
            }
            break
        case `Quit`:
            for (qns of consoleQuestions.Quit) { console.log(qns) }
            switch (input.questionInt(">>>>")) {
                case 1:
                    console.clear()
                    question(`Start`)
                case 0:
                    console.log("Thank you, Good Bye")
                    process.exit()
                default:
                    console.clear()
                    question(`Quit`)
            }
            break
        case `Order`:
            for (qns of consoleQuestions.Order) { console.log(qns) }
            switch (input.questionInt(">>>>")) {
                case 1:
                    sendOrder()
                    break
                case 2:
                    question(`removeItem`)
                    break
                case 0:
                    question(`Start`)
                default:
                    console.clear()
                    question(`Order`)
            }
            break
        case `removeItem`:
            for (qns of consoleQuestions.removeItem) { console.log(qns) }
            orderCart.removeItem(getInput(orderCart.getCart().slice(1, -1).split('\n')))
            question(`Start`)
            break
    }
}

function showMenu() {
    let item
    let check
    let quantity = 0
    let extraOption = []

    //console.log All Categories
    console.log(`Select Category`)
    Categories = menu.getCategory()
    num = 1
    for (let category of Categories) {
        console.log(`${num}. ${category}`)
        num++
    }
    console.log(`0. Cancel Selection`)
    //console.log All Dishes
    Dishes = menu.getDish(Categories[getInput(Categories)])
    console.log(`\tSelect Dish`)
    num = 1
    for (let dish of Dishes) {
        console.log(`\t${num}. ${dish.code}: ${dish.price} - ${dish.name}`)
        num++
    }
    console.log(`\t0. Cancel Selection`)
    item = Dishes[getInput(Dishes)]

    //Check for empty options
    for (let x of item.option) {
        check += x.join("")
    }
    //console.log All Options
    Options = item.option
    if (check != "undefined") {
        for (let option of Options) {
            console.log(`\t\tSelect Option`)
            num = 1
            for (let choice of option) {
                console.log(`\t\t${num}. ${choice}`)
                num++
            }
            console.log(`\t\t0. Cancel Selection`)
            extraOption.push(option[getInput(option)])
        }
    }
    //Get Quantity
    console.log("Enter Order Quantity")
    do {
        quantity = input.questionInt(">>>> ")
    } while (quantity <= 0);
    orderCart.updateCart(quantity, item.name, item.price, extraOption)
    // Print success message including what the user bought
    console.clear()
    console.log(`\n\n\nSuccessfully added to cart - QTY: ${quantity} X ${item.name} - ${extraOption.filter(Boolean)}` + "\n\n\n")
    input.question("Press Enter to continue...")
    console.clear()
    question(`Start`)
}

function showCart() {
    if (orderCart.getCart() == "\n") {
        console.clear()
        console.log("\nPlease add something to your cart.\n")
        input.question("Press Enter to continue...")
        console.clear()
        question(`Start`)
    }
    console.log("Your cart:")
    console.log("===============================================================")
    console.log(orderCart.getCart())
    console.log("===============================================================")
    console.log(`Total Cost: $${orderCart.getPrice()}`)
    question(`Order`)
}

function getInput(check) {
    //necessary to return select properly
    function checkInvalid(check) {
        select = input.questionInt(">>>>")
        if (select == 0) {
            question(`Start`)
        }
        else if (select > check.length) {
            checkInvalid(check)
        }
        return select
    }
    checkInvalid(check)
    return select - 1
}

function sendOrder() {
    //Get valid visa card details
    do {
        var cardNum = input.question("Enter Visa Card(4444111122223333)\n0. Exit\n>>>> ")
        if (cardNum == 0) { question(`Start`) }
    } while (!cardNum.match(/^(?:4[0-9]{12}(?:[0-9]{3})?)$/))

    //Get valid card expiry date
    do {
        var cardExp = input.question("Enter card expiry(MM/YY)\n0. Exit\n>>>>")
        if (cardExp == 0) { question(`Start`) }
    } while (!cardExp.match(/^(0[1-9]|1[012])\/\d\d$/))

    //Get valid security code 
    do {
        var cardSec = input.question("Enter card security code\n0. Exit\n>>>> ")
        if (cardSec == 0) { question(`Start`) }
    } while (!cardSec.match(/^\d\d\d$/))

    //Get address
    let address = input.question("Enter address\n>>>> ")

    let uuid = uuidv4(); // User unique ID
    //This is meant for linux only!!!
    fs.appendFileSync(`orders\\${uuid}.txt`,`${orderCart.getCart()}\nPrice: $${orderCart.getPrice()}\nUUID: ${uuid}\nCard Number: ${cardNum}\nCard Expiry Date: ${cardExp}\nCard Security Code: ${cardSec}\nAddress: ${address}\n` + "===============================================================\n", (err) => {
        if (err) throw err
    })

    console.log(`Your unique user ID: ${uuid}`)
    input.question("Press Enter to continue...")
    console.clear()
    orderCart.clearItem()
    question(`Start`)
}

let consoleQuestions = {
    Start: [`Welcome to NiceMeal Restaurant`, `1. View Menu`, `2. View Cart`, `0. Quit`],
    Quit: [`Are you sure?`, `1. No`, `0. Yes`],
    Order: [`Enter cart option`, `1. Send Order`, `2. Remove item`, `0. Back to main`],
    removeItem: [`\tRemove item`, `\tEnter item number`, `\t0. Back to main`],
}

orderCart = new Cart()
menu = new Menu()
question(`Start`)