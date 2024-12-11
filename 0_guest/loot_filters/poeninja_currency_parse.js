// all the other

worth_to_get = []
min_value = 0.8

divine_orb_price = 150
items = Array.from(document.querySelector('tbody').querySelectorAll('tr'))



items.map(el=>{
  item_name = el.querySelectorAll('td')[0].querySelector('span').textContent;
  price = Number(el.querySelectorAll('td')[1].textContent)
  if (price >= min_value){
    worth_to_get.push(item_name)
  }
})
console.log((`"`) + worth_to_get.join(`" "`) + (`"`))

//

// currency
worth_to_get = []
min_value = 1.7
items = Array.from(document.querySelector('tbody').querySelectorAll('tr'))



items.map(el=>{
  item_name = el.querySelectorAll('td')[0].textContent;
  price = Number(el.querySelectorAll('td')[3].textContent)
  if (price <= min_value){
    worth_to_get.push(item_name)
  }
})
console.log((`"`) + worth_to_get.join(`" "`) + (`"`))

// clusters

worth_to_get = []
min_value = 50
items = Array.from(document.querySelector('tbody').querySelectorAll('tr'))

items.map(item=>{
  item_name = item.querySelectorAll('td')[0].textContent;
  multiplier = 1
  if (item.querySelectorAll('td')[3].querySelector('img').title == 'Divine Orb'){
    multiplier = divine_orb_price
  }
  price = Number(item.querySelectorAll('td')[3].textContent) * multiplier
  if (price >= min_value){
    worth_to_get.push(item_name)
  }
})
console.log((`"`) + worth_to_get.join(`" "`) + (`"`))



// gems to exp



document.querySelector('div[class="item-overview"]').querySelector('button').click()

var expandMultipleTimes = async ()=>{
  for (i = 0; i < 10; i++) {
    document.querySelector('div[class="item-overview"]').querySelector('button').click()
    await new Promise (res => setTimeout (res, 1000));
  }  

}

gems = {

}

items = Array.from(document.querySelector('tbody').querySelectorAll('tr'))

items.map(item=>{
  item_name = item.querySelectorAll('td')[0].querySelector('span').textContent
  multiplier = 1
  if (item.querySelectorAll('td')[4].querySelector('img').title== 'Divine Orb'){
    multiplier = divine_orb_price
  }
  price = Number(item.querySelectorAll('td')[4].textContent) * multiplier
  level = Number(item.querySelectorAll('td')[1].textContent)
  quality = Number(item.querySelectorAll('td')[2].textContent)
  corrupt = item.querySelectorAll('td')[3].textContent
  if (gems[item_name] == null){
    gems[item_name] = []
  }
  // if (items[0].querySelectorAll('td')[4].querySelector('svg') == null){}
  gems[item_name].push({item_name, level,quality, corrupt, price})
})

possible_to_lvl = []


for (let item in gems) {
  has_lvl_1_gem = false;
  gem_name = ''
  let item_array = gems[item]
  
  if (item_array.length == 1){
    continue
  }
  min_price = 0
  max_price = 0
  for (let i of item_array){
    if (i.quality == 23){
      continue
    }

    if (i.level == 1){
      console.log(`${i} has lvl 1 gem`)
      has_lvl_1_gem = true
      min_price = i.price
    }
    if (i.level == 20){
      console.log(`${i} has lvl 20 gem`)
      if (max_price < i.price){
        max_price = i.price
      }
    }
    if (i.level == 5){
      console.log(`${i} has lvl 5 gem`)
      if (max_price < i.price){
        max_price = i.price
      }
      
    }
  }
  if (has_lvl_1_gem == true){
    reworked_gem_info = {

    }
    reworked_gem_info.gem_name = item_array[0].item_name
    reworked_gem_info.min_price = min_price
    reworked_gem_info.max_price = max_price
    reworked_gem_info.possible_profit = max_price - min_price
    reworked_gem_info.raw_data = item_array
    possible_to_lvl.push(reworked_gem_info)
  }
}

possible_to_lvl.sort(function(a, b) {
  return a.possible_profit - b.possible_profit;
});
