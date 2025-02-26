```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +FrontendServices
    +API
}
class BusinessLogicLayer {
    +baseModel
    +UserModel
    +PlaceModel
    +ReviewsModel
    +AmenityModel

}
class PersistenceLayer {
    +DatabaseAccess
}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
```
