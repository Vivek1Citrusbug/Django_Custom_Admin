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
      url: window.datatable_url,
      type: "get",
    },
    columns: [
      { data: "id",name:"id"},
      { data: "username",name: "username"},
      { data: "first_name",name: "first_name"},
      { data: "last_name",name: "first_name"},
      { data: "email", name: "email" },
      { data: "date_joined", name: "date_joined" },
      { data: "is_active", name: "is_active" },
      { data: "is_staff", name: "is_staff" },
      { data: "last_login", name: "last_login" },
      {
        render: function (data, type, JsonResultRow, meta) {
          return `
            <div class="d-flex justify-content-between">
              <!-- Update Icon -->
              <a href="/customadmin/user/${JsonResultRow.id}/update" class="link-dark mr-5">
                <i style="font-size:24px" class="fa mr-5">&#xf040; </i>
              </a>
    
              <!-- Delete Icon -->
              <a href="/customadmin/user-delete/${JsonResultRow.id}/delete" class="link-dark" onclick="deleteUser(${JsonResultRow.id})">
                <i style="font-size:24px" class="fa"> &#xf1f8;</i>
              </a>
            </div>
          `;
        },
      },
    ],
    columnDefs: [{ orderable: false, targets: [1, 6] }],
    order: [[3, "desc"]],
    oLanguage: {
      sSearch: "",
      oPaginate: {
        sNext: `<a href="#" aria-controls="user-table" data-dt-idx="4" tabindex="0" class="page-link">></a>`,
        sPrevious: `<a href="#" aria-controls="user-table" data-dt-idx="0" tabindex="0" class="page-link"><</a>`,
      },
    },
  });

  table.on("click", "tbody tr", function () {
    location.href = `/customadmin/user/${table.row(this).data().id}`
  });

});
