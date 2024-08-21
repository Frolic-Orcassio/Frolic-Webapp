/**
* Template Name: NiceAdmin
* Template URL: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/
* Updated: Apr 20 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function () {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function (e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function (e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
            color: []
          },
          {
            background: []
          }
          ],
          [{
            script: "super"
          },
          {
            script: "sub"
          }
          ],
          [{
            list: "ordered"
          },
          {
            list: "bullet"
          },
          {
            indent: "-1"
          },
          {
            indent: "+1"
          }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
    });
  }

  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**********************************************************
  * Custom js ***********************************************
  **********************************************************/

  /**
   * sidebar nav item selection
   */
  let navItems = document.querySelectorAll('#sidebar .nav-item');
  navItems.forEach(item => {
    if (!(item.querySelector('a').classList.contains('nav-dropdown'))) {
      item.addEventListener('click', function (event) {
        let navItemss = document.querySelectorAll('#sidebar .nav-item');

        navItemss.forEach(itemm => {
          let anchor = itemm.querySelector('a')
          if (!(anchor.classList.contains('collapsed'))) {
            anchor.classList.add('collapsed')
          }
          if (anchor.classList.contains('nav-dropdown')) {
            new bootstrap.Collapse(anchor.getAttribute('data-bs-target'), { toggle: false }).hide()
            itemm.querySelectorAll('.nav-dropdown-item').forEach((dropdown_item) => {
              let item_anchor = dropdown_item.querySelector('a')
              if (item_anchor.classList.contains('active')) {
                item_anchor.classList.remove('active')
              }
            })
          }
        })

        item.querySelector('a').classList.remove('collapsed')
      });
    }
  });

  let navDropdownItems = document.querySelectorAll('#sidebar .nav-dropdown-item')
  navDropdownItems.forEach(item => {
    item.addEventListener('click', function (event) {
      let navItemss = document.querySelectorAll('#sidebar .nav-item');
      let navDropdownItemss = document.querySelectorAll('#sidebar .nav-dropdown-item')

      navItemss.forEach(itemm => {
        let anchor = itemm.querySelector('a')
        if (!(anchor.classList.contains('nav-dropdown'))) {
          if (!(anchor.classList.contains('collapsed'))) {
            anchor.classList.add('collapsed')
          }
        }
      })

      navDropdownItemss.forEach(itemm => {
        let anchor = itemm.querySelector('a')
        if (anchor.classList.contains('active')) {
          anchor.classList.remove('active')
        }
      })

      item.querySelector('a').classList.add('active')
      event.stopPropagation();
    })
  })


  document.addEventListener('createEditor', function () {
    new Quill('#editor', {
      modules: {
        toolbar: [
          [{ header: [1, 2, false] }],
          ['bold', 'italic', 'underline'],
          ['image', { 'list': 'ordered'}, { 'list': 'bullet' }, { 'align': [] }, 'link'],
        ],
      },
      placeholder: 'Start designing event page here...',
      theme: 'snow', // or 'bubble'
    });
  })


  document.addEventListener('userDeleted', function() {
    document.querySelectorAll('.modal').forEach(element => {
      bootstrap.Modal.getOrCreateInstance(element).hide()
    });
    document.getElementById('usersReload').click()
  })

  /**
   * END MAIN JS
  */
})();