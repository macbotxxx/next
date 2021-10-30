
const url = window.location.href
const searchFormMobile = document.getElementById('search-form-mobile')
const searchInputMobile = document.getElementById('search-input-mobile')
const resultsBoxMobile = document.getElementById('results-box-mobile')
console.log('michael mobile')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value


// const sendSearchData = (product) => {
//     $.ajax({
//         type: 'POST',
//         url : '/search/',
//         data: {
//             'csrfmiddlewaretoken': csrf,
//             'product': product,
//         },
//         success: (res) => {
//             const data = res.data
//             if (Array.isArray(data)) {
//                 resultsBoxMobile.innerHTML = ""
//                 data.forEach(product => {
//                     resultsBoxMobile.innerHTML += `
//                     <ul class="list-result">
//                         <li class="cart-item">
//                             <div class="ps-product--mini-cart"><a href="/product-details/${product.slug}/"><img class="ps-product__thumbnail" src="${product.image}" alt="alt" /></a>
//                                 <div class="ps-product__content"><a class="ps-product__name" href="/product-details/${product.slug}/">${product.product_name}</a>
//                                     <p class="ps-product__meta"> <span class="ps-product__price">₦${product.price}</span>
//                                     </p>
//                                 </div>
//                             </div>
//                         </li>
//                     </ul> 
//                     `
//                 })
                
//             }else{
//                 if (searchInputMobile.value.length > 0){
//                     resultsBoxMobile.innerHTML = `<b>${data}</b>`
//                 }else{
//                     resultsBoxMobile.classList.add('not-visible')
//                 }
//             }
//         }, 

//         error: (err) => {
//             console.log('err')
//         }

//     })
// }


searchInputMobile.addEventListener('keyup', e=>{
    console.log(e.target.value)
    // if (resultsBoxMobile.classList.contains('not-visible')){
    //     resultsBoxMobile.classList.remove('not-visible')
    // }

    // sendSearchData(e.target.value)
})



