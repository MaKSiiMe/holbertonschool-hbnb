```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +FrontendServices
    +API
}
class BusinessLogicLayer {
    +User
    +Place
    +Reviews
    +Amenity

}
class PersistenceLayer {
    +DatabaseAccess
}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
```
