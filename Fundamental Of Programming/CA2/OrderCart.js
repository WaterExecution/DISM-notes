class orderCart{
    constructor(){
        this.cart = []
    }

    getCart(){
        let cart = "\n"
        let num = 1
        for (let item of this.cart){
            cart += `${num}. QTY: ${item[0]}\tX ${item[1]} - ${[item[3],item[4]].filter(Boolean)} - $${parseFloat(item[2].substring(4)).toFixed(2)}\n`
            num++
        }
        return cart
    }

    getPrice(){
        let price = 0
        for (let item of this.cart){
            price += parseFloat(item[2].substring(4))*item[0]
        }
        return price.toFixed(2)
    }

    removeItem(select){
        this.cart.splice(select-1,1)
    }

    clearItem(){
        this.cart = []
    }
    
    updateCart(quantity, name, price, extra){
        this.cart.push([quantity, name, price, extra].filter(Boolean))
    }
}

module.exports = orderCart;