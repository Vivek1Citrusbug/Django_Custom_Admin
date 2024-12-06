$(document).ready(function () {
  let table = $("#user-table").DataTable({
    paging: true,
    responsive: true,
    pageLength: 10,
    autoWidth: false,
    lengthMenu: [10, 25, 50, 100],
    searching: true,
    processing: true,
    serverSide: true,
    ajax: {
      // context: this,
      url: window.datatable_url,
      type: "get",
    },
    columns: [
      { data: "id", name: "id", },
      { data : "profile_picture" ,name : "profile_picture",
        render: function (data, type, JsonResultRow, meta) {
          let profile_picture = JsonResultRow.profile_picture ? JsonResultRow.profile_picture : '/static/images/default-user-profile-photo.png';
          return `<img src="${profile_picture}" alt="Profile Picture" class="profile-img" style="width: 40px; height: 40px; border-radius: 50%;"></img>`
        },
      },
      { data: "username", name: "username", },
      { data: "first_name", name: "first_name" },
      { data: "last_name", name: "last_name" },
      { data: "email", name: "email" },
      { data: "date_joined", name: "date_joined" },
      { data: "is_active", name: "is_active" },
      { data: "is_staff", name: "is_staff" },
      { data: "last_login", name: "last_login" },
      { data: "action", name: "action"},
    ],
    // columnDefs: [{ orderable: false, targets: [1, 6] }],
    order: [[0, "asc"]],
    oLanguage: {
      sSearch: "",
      oPaginate: {
        sNext: `<a href="#" aria-controls="user-table" data-dt-idx="4" tabindex="0" class="page-link">></a>`,
        sPrevious: `<a href="#" aria-controls="user-table" data-dt-idx="0" tabindex="0" class="page-link"><</a>`,
      },
    },
  });

  // table.on("click", "tbody tr", function () {
  //   location.href = `/customadmin/user/${table.row(this).data().id}`
  // });
  
// };

});
