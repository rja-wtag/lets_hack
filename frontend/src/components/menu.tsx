import { Link } from "react-router-dom";

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from "@/components/ui/navigation-menu";

export default function MainMenu() {
  return (
    <section className="flex justify-center">
      <NavigationMenu className="relative flex justify-center w-100">
        <NavigationMenuList>
          <NavigationMenuItem>
            <NavigationMenuLink className="text-lg" asChild>
              <Link to="/">Home</Link>
            </NavigationMenuLink>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <NavigationMenuLink className="text-lg" asChild>
              <Link to="/projects">projects</Link>
            </NavigationMenuLink>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <NavigationMenuLink className="text-lg" asChild>
              <Link to="/projects">About us</Link>
            </NavigationMenuLink>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <NavigationMenuLink className="text-lg" asChild>
              <Link to="/projects">Contact us</Link>
            </NavigationMenuLink>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
    </section>
  );
}
