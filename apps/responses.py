from apps import schemas

get_users_current = {
    400: {"model": schemas.ErrorResponseModel},
    401: {"model": schemas.HttpBaseError,
          "content": {
              "application/json": {
                  "example": {"title": "Response 401 Current User Users Current Get"}
                                 }
                    }
      }}

get_users = {
    400: {"model": schemas.ErrorResponseModel,
                          },
    401: {"model": schemas.HttpBaseError,
          "content": {
              "application/json": {
                  "example": {"title": "Response 401 Users Users Get"}
              }
          }
          }}

patch_users_pk = {
    400: {"model": schemas.ErrorResponseModel},
    401: {"model": schemas.HttpBaseError,
          "content": {
              "application/json": {"example": {"title": "Response 401 Edit User Users  Pk  Patch"}}
                    }
          },
    404: {"model": schemas.HttpBaseError,
          "content": {
              "application/json": {"example": {"title": "Response 404 Edit User Users  Pk  Patch"}}
                    }
          }
    }

get_private_users = {
     400: {"model": schemas.ErrorResponseModel},
     401: {"model": schemas.HttpBaseError,
           "content": {
               "application/json": {"example": {"title": "Response 401 Private Users Private Users Get"}}
           }
           },
     403: {"model": schemas.HttpBaseError,
           "content": {
               "application/json": {"example": {"title": "Response 403 Private Users Private Users Get"}}
                     }
           }
    }

post_private_users = {
     400: {"model": schemas.ErrorResponseModel},
     401: {"model": schemas.HttpBaseError,
           "content": {
               "application/json": {"example": {"title": "Response 401 Private Create Users Private Users Post"}}
           }
           },
     403: {"model": schemas.HttpBaseError,
           "content": {
               "application/json": {"example": {"title": "Response 403 Private Create Users Private Users Post"}}
                    }
           }
     }

get_private_users_pk = {
    400: {"model": schemas.ErrorResponseModel},
    401: {"model": schemas.HttpBaseError,
          "content": {
              "application/json": {
                  "example": {"title": "Response 401 Private Get User Private Users  Pk  Get"}
              }
          }
          },
    403: {"model": schemas.HttpBaseError,
          "content": {
              "application/json": {
                  "example": {"title": "Response 403 Private Get User Private Users  Pk  Get"}
              }
          }
          },
    404: {"model": schemas.HttpBaseError,
          "content": {
              "application/json": {
                  "example": {"title": "Response 404 Private Get User Private Users  Pk  Get"}
              }
          }
          }
     }

delete_private_users_pk = {
    400: {"model": schemas.ErrorResponseModel},
    401: {"model": schemas.HttpBaseError,
         "content": {
             "application/json": {
                 "example": {"title": "Response 401 Private Delete User Private Users  Pk  Delete"}
             }
         }
         },
    403: {"model": schemas.HttpBaseError,
         "content": {
             "application/json": {
                 "example": {"title": "Response 403 Private Delete User Private Users  Pk  Delete"}
             }
         }
         },
    404: {"model": schemas.HttpBaseError,
         "content": {
             "application/json": {
                 "example": {"title": "Response 404 Private Delete User Private Users  Pk  Delete"}
             }
         }
         }
    }


patch_private_users_pk = {
    400: {"model": schemas.ErrorResponseModel},
    401: {"model": schemas.HttpBaseError,
         "content": {
             "application/json": {
                 "example": {"title": "Response 401 Private Patch User Private Users  Pk  Patch"}
             }
         }
         },
    403: {"model": schemas.HttpBaseError,
         "content": {
             "application/json": {
                 "example": {"title": "Response 403 Private Patch User Private Users  Pk  Patch"}
             }
         }
         },
    404: {"model": schemas.HttpBaseError,
         "content": {
             "application/json": {
                 "example": {"title": "Response 404 Private Patch User Private Users  Pk  Patch"}
                                 }
                    }
         }
    }