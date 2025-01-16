document.addEventListener("DOMContentLoaded", function() {
  var titleInput = document.getElementById("id_title"); // ID поля 'title'
  var slugInput = document.getElementById("id_slug"); // ID поля 'slug'

  titleInput.addEventListener("input", function() {
    var title = titleInput.value;
    var slug = '';

    // Преобразование текста в валидный URI формат
    slug = encodeURIComponent(title)
      .replace(/[^\w\s-]/g, '') // Удаление всех символов, кроме латинских букв, цифр, знаков подчеркивания и дефиса
      .replace(/[\s_-]+/g, '-') // Замена пробелов и знаков подчеркивания на дефисы
      .replace(/[^\w-]/g, ''); // Удаление любых оставшихся символов

    slugInput.value = slug;
  });
});